from unittest.mock import patch

from django.test import TestCase

from properties.exceptions.property import PropertyException
from properties.services.property import PropertyService
from properties.tests.mock import (
    PROPERTY_PROVIDER_1_MOCKED,
    PROPERTY_PROVIDER_2_MOCKED,
)


class PropertyServiceTests(TestCase):
    
    @patch(
        "properties.providers.property.provider_1.PropertyProvider1.get_property",
        return_value=PROPERTY_PROVIDER_1_MOCKED
    )
    @patch(
        "properties.providers.property.provider_2.PropertyProvider2.get_property",
        return_value=PROPERTY_PROVIDER_2_MOCKED,
    )
    def test_get_property_by_address_success(self, *_):
        address = "123%20Main%20St,%20Anytown,%20USA"
        result = PropertyService.get_property_by_address(address)

        self.assertEqual(result["normalized_address"], "123 Main St, Anytown, USA")
        self.assertEqual(result["square_footage"], 2000)
        self.assertEqual(result["lot_size_acres"], 1.6)  # It should prioritize Provider 2
        self.assertEqual(result["year_built"], 1990)
        self.assertEqual(result["property_type"], "House")
        self.assertEqual(result["bedrooms"], 3)
        self.assertEqual(result["bathrooms"], 2)
        self.assertEqual(result["room_count"], 2)  # It should prioritize Provider 2
        self.assertFalse(result["septic_system"])  # It should prioritize Provider 2
        self.assertEqual(result["sale_price"], 250000)

    @patch(
        "properties.providers.property.provider_1.PropertyProvider1.get_property",
        side_effect=PropertyException(PropertyException.ErrorCode.Unauthorized)
    )
    @patch(
        "properties.providers.property.provider_2.PropertyProvider2.get_property",
        side_effect=PropertyException(PropertyException.ErrorCode.Unauthorized)
    )
    def test_get_property_by_address_failure(self, *_):
        address = "123%20Main%20St,%20Anytown,%20USA"
        result = PropertyService.get_property_by_address(address)

        self.assertIn("error", result)
        self.assertEqual(result["error"], "Both providers failed to retrieve property data.")
        self.assertEqual(len(result["details"]), 2)

    @patch(
        "properties.providers.property.provider_1.PropertyProvider1.get_property",
        side_effect=PropertyException(PropertyException.ErrorCode.Unauthorized)
    )
    @patch(
        "properties.providers.property.provider_2.PropertyProvider2.get_property",
        return_value=PROPERTY_PROVIDER_2_MOCKED,
    )
    def test_get_property_if_some_provider_fails(self, *_):
        address = "123%20Main%20St,%20Anytown,%20USA"
        result = PropertyService.get_property_by_address(address)

        # It should use Provider 2  because Provider 1 failed
        self.assertEqual(result["normalized_address"], "123 Main Street, Anytown, USA")  
        self.assertEqual(result["square_footage"], 1900)
        self.assertEqual(result["lot_size_acres"], 1.6)
        self.assertEqual(result["year_built"], 1992)
        self.assertEqual(result["property_type"], "Single Family Home")
        self.assertEqual(result["bedrooms"], 3)
        self.assertEqual(result["bathrooms"], 2)
        self.assertEqual(result["room_count"], 2)
        self.assertFalse(result["septic_system"])
        self.assertEqual(result["sale_price"], 245000)

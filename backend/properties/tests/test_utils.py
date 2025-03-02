from django.test import TestCase

from parameterized import parameterized

from properties.utils.conversion  import sqft_to_acre


class PropertyConversionTests(TestCase):
    @parameterized.expand([
        (0, 0),
        (87120, 2),
        (10000, 0.2295684113865932),
    ])
    def test_sqft_to_acre(self, sqft, expected_value):
        result = sqft_to_acre(sqft)

        self.assertEqual(result, expected_value)

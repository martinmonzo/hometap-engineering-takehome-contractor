from properties.exceptions.property import PropertyException
from properties.providers.property.provider_1 import PropertyProvider1
from properties.providers.property.provider_2 import PropertyProvider2
from properties.utils.conversion  import sqft_to_acre


class PropertyService:
    """
    Service with all logic related to Properties
    """
    providers = [PropertyProvider1, PropertyProvider2]

    @classmethod
    def get_property_by_address(cls, address: str) -> dict:
        """
        Retrieves relevant information about a property given its address

        Args:
            address: The direction of the property

        Returns:
            dict with property information or providers errors
        """
        response = {}
        errors = []

        for provider in cls.providers:
            try:
                response[provider.NAME] = provider.get_property(address)
            except PropertyException as exc:
                errors.append({
                    "provider": provider.NAME,
                    "error": exc.message,
                    "status_code": exc.status_code
                })

        if len(errors) == len(cls.providers):  # If every provider failed
            return {
                "error": "Both providers failed to retrieve property data.",
                "details": errors,
            }

        return cls._process_data(**response)

    @classmethod
    def _process_data(cls, **kwargs: dict) -> dict:
        """Processes data from different providers and retrieves it normalized"""
        provider_1_data = kwargs.get("provider_1", {})
        provider_2_data = kwargs.get("provider_2", {})
        
        return {
            "normalized_address": provider_1_data.get("formattedAddress", provider_2_data.get("NormalizedAddress")),
            "square_footage": provider_1_data.get("squareFootage", provider_2_data.get("SquareFootage")),
            # For lot size, we try to obtain it first from provider2 because it already retrieves it in acres, so we avoid unit conversion
            "lot_size_acres": provider_2_data.get("LotSizeAcres", sqft_to_acre(provider_1_data.get("lotSizeSqFt", 0))),
            "year_built": provider_1_data.get("yearBuilt", provider_2_data.get("YearConstructed")),
            "property_type": provider_1_data.get("propertyType", provider_2_data.get("PropertyType")),
            "bedrooms": provider_1_data.get("bedrooms", provider_2_data.get("Bedrooms")),
            "bathrooms": provider_1_data.get("bathrooms", provider_2_data.get("Bathrooms")),
            # For room_count and septic_system, we try to obtain them first from provider2 because it already retrieves them directly,
            # while provider1 accesses them indirectly through the key 'features'
            "room_count": (
                provider_2_data.get("RoomCount")
                if provider_2_data.get("RoomCount") is not None
                else provider_1_data.get("features", {}).get("roomCount")
            ),
            "septic_system": (
                provider_2_data.get("SepticSystem")
                if provider_2_data.get("SepticSystem") is not None
                else provider_1_data.get("features", {}).get("septicSystem")
            ),
            "sale_price": provider_1_data.get("lastSalePrice", provider_2_data.get("SalePrice")),
        }

import requests

from properties.exceptions.property import PropertyException


class PropertyProviderBase:
    """
    This class contains the base logic for all providers that are related to properties and have the same methods.
    To inherit from PropertyProviderBase, just create a class that extends from it, and add it a BASE_URL and API_KEY
    """
    NAME: str
    BASE_URL: str
    API_KEY: str

    @classmethod
    def get_property(cls, address: str) -> dict:
        # BASE_URL and API_KEY must be overriden in subclasses
        if not hasattr(cls, "BASE_URL") or not hasattr(cls, "API_KEY"):
            raise PropertyException(PropertyException.ErrorCode.Missing_Settings)

        headers = {
            "X-API-KEY": cls.API_KEY,
            "Accept": "application/json"
        }
        params = {"address": address}

        response = requests.get(cls.BASE_URL, headers=headers, params=params)
        if response.status_code == 401:
            raise PropertyException(PropertyException.ErrorCode.Unauthorized)
        if response.status_code != 200:
            raise PropertyException(PropertyException.ErrorCode.Unknown_Error)

        # If response is successful
        return response.json()["data"]

    # Add below more common methods to different providers

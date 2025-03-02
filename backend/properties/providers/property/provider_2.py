import os

from dotenv import load_dotenv

from properties.providers.property.base import PropertyProviderBase

load_dotenv()


class PropertyProvider2(PropertyProviderBase):
    BASE_URL: str = os.getenv("PROVIDER_2_BASE_URL")
    API_KEY: str = os.getenv("PROVIDER_2_API_KEY")

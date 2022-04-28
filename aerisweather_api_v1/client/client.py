"""
aerisweather_api_v1/client/client
---------------------------------

Contains code for the Aeris API v1 client.
"""

from ..deserializers.common import make_deserialize_try_geojson
from ..deserializers.airquality import deserialize_airquality
from .airquality import AerisApiAirQualityEndpoint
from .http import AerisApiHttpClient


class AerisApiClient:
    """
    Client for the Aeris API v1.

    This client provides a Python-native interface to the Aeris API. This is
    the recommended way to interact with the Aeris API.

    You probably want to create one of these using :py:func:`aeris_api_client`.
    """

    def __init__(self, http_client: AerisApiHttpClient, strip_http_response_content: bool) -> None:
        self.http = http_client

        self.airquality = AerisApiAirQualityEndpoint(
            http_client,
            make_deserialize_try_geojson(deserialize_airquality),
            strip_http_response_content,
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(http_client={self.http})"

"""
aerisweather_api_v1/client
--------------------------

Contains code defining the Aeris API v1 client.
"""

from typing import Optional

from .client import AerisApiClient
from .http import AerisApiHttpClient


def aeris_api_client(client_id: str, client_secret: str, base_url: Optional[str] = None) -> AerisApiClient:
    """
    Given a client ID and client secret, constructs and returns an
    appropriate :py:class:`AerisApiClient`. This is the preferred method
    for creating a usable client ot the Aeris API.

    :param client_id: AerisWeather client ID used to make the request; \
        you can get one by :aerissignup:`signing up for an AerisWeather API subscription <>`
    :param client_secret: AerisWeather client secret used to make the request; \
        you can get one by :aerissignup:`signing up for an AerisWeather API subscription <>`
    :param base_url: base URL against which Aeris API requests should be made; \
        this can be overridden if you have implemented a proxy for caching
    """
    if base_url is None:
        http_client = AerisApiHttpClient(client_id, client_secret)
    else:
        http_client = AerisApiHttpClient(client_id, client_secret, base_url=base_url)

    return AerisApiClient(http_client)


__all__ = [
    "aeris_api_client",
    "AerisApiClient",
    "AerisApiHttpClient",
]

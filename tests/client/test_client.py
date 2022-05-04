"""
tests/client/test_endpoint
--------------------------

Tests functionality in the aerisweather_api_v1.client.client module.
"""

from typing import Any

import pytest
import requests

from aerisweather_api_v1.client.client import AerisApiClient
from aerisweather_api_v1.client.http import AerisApiHttpClient
from aerisweather_api_v1.client.airquality import AerisApiAirQualityEndpoint


@pytest.fixture(params=[True, False])
def strip_http_response_content(request: Any) -> bool:
    # to satisfy mypy
    assert request.param is True or request.param is False

    return request.param


@pytest.fixture
def aeris_api_client(mock_session: requests.Session, strip_http_response_content: bool) -> AerisApiClient:
    """
    Creates an :py:class:`AerisApiClient` for testing.
    """
    http = AerisApiHttpClient("client_id", "client_secret", requests_session=mock_session)

    return AerisApiClient(http, strip_http_response_content)


class TestAerisApiClient:
    """
    Tests the functionality of the :py:class:`AerisApiClient`.
    """

    def test_repr(self, aeris_api_client: AerisApiClient) -> None:
        """
        Tests that :py:meth:`AerisApiClient.__repr__` returns a string.
        """
        assert isinstance(aeris_api_client.__repr__(), str)

    def test_airquality_endpoint(self, aeris_api_client: AerisApiClient, strip_http_response_content: bool) -> None:
        """
        Tests that the airquality endpoint is initialized correctly.
        """
        assert isinstance(aeris_api_client.airquality, AerisApiAirQualityEndpoint)
        assert aeris_api_client.airquality.strip_http_response_content == strip_http_response_content

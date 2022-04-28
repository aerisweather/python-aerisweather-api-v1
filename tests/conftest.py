"""
tests/conftest
--------------

This file contains global fixtures and configuration for pytest.
"""

import pytest

from aerisweather_api_v1.client import AerisApiClient, AerisApiHttpClient

from testhelper.requests import MockSession


@pytest.fixture
def aeris_api_mock_client(mock_url: str, mock_session: MockSession) -> AerisApiClient:
    """
    Provides an AerisApiClient mock client for testing.
    """
    client_id = "AERISWEATHER_API_V1_TEST"
    client_secret = "AERISWEATHER_API_V1_TEST_SECRET"
    http = AerisApiHttpClient(
        client_id,
        client_secret,
        base_url=mock_url,
        requests_session=mock_session,
    )
    return AerisApiClient(http, strip_http_response_content=False)


@pytest.fixture
def mock_url() -> str:
    """
    The URL that is used for mock requests.
    """
    return "http://localhost:3333"


@pytest.fixture
def mock_session() -> MockSession:
    return MockSession()

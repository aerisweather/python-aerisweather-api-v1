"""
tests/client/test_init
----------------------

Tests functionality in the aerisweather_api_v1.client.__init__ module.
"""

from os import environ
from typing import Optional

import pytest

from aerisweather_api_v1.client import aeris_api_client, AerisApiClient


class TestAerisApiClientFactory:
    """
    Tests the functionality of the :py:func:`aeris_api_client` factory.
    """

    def test_no_base_url(self) -> None:
        """
        Tests that an appropriate :py:class:`AerisApiClient` is created when
        a ``base_url`` is not passed.
        """

        client_id = "test_no_base_url_client_id"
        client_secret = "test_no_base_url_client_secret"
        client = aeris_api_client(client_id, client_secret)

        assert isinstance(client, AerisApiClient)
        assert client.http.client_id == client_id
        assert client.http.client_secret == client_secret
        assert client.http.base_url == "https://api.aerisapi.com"
        assert client.airquality.strip_http_response_content is True

    @pytest.mark.parametrize(
        "base_url",
        [
            # Test passing None, which should give us the default base_url.
            None,
            # Test passing the default base_url value.
            "https://api.aerisapi.com",
            # Test passing the default base_url value but using http.
            "http://api.aerisapi.com",
            # Test passing a custom base_url using https.
            "https://proxy.aerisapi.example.com",
            # Test passing a custom base_url using http.
            "http://proxy.aerisapi.example.com",
        ],
    )
    def test_custom_base_url(self, base_url: Optional[str]) -> None:
        """
        Tests that an appropriate :py:class:`AerisApiClient` is created when
        a ``base_url`` is passed.
        """
        if base_url is None:
            expected_base_url = "https://api.aerisapi.com"
        else:
            expected_base_url = base_url
        client_id = "test_custom_base_url_client_id"
        client_secret = "test_custom_base_url_client_secret"

        client = aeris_api_client(client_id, client_secret, base_url)
        assert client.http.client_id == client_id
        assert client.http.client_secret == client_secret
        assert client.http.base_url == expected_base_url
        assert client.airquality.strip_http_response_content is True

    @pytest.mark.parametrize("val", ["1", "t", "true", "y", "yes"])
    def test_strip_http_response_content_explicit_true(self, val: str) -> None:
        """
        Tests that the :py:class:`AerisApiClient` is configured to strip HTTP
        response content when the required environment variable is explicitly
        set to a truthy value.
        """
        environ["AERISWEATHER_API_V1_STRIP_HTTP_RESPONSE_CONTENT"] = val
        client = aeris_api_client("client_id", "client_secret")

        assert client.airquality.strip_http_response_content is True

    @pytest.mark.parametrize("val", ["0", "f", "false", "n", "no"])
    def test_strip_http_response_content_explicit_false(self, val: str) -> None:
        """
        Tests that the :py:class:`AerisApiClient` is configured to strip HTTP
        response content when the required environment variable is explicitly
        set to a falsy value.
        """
        environ["AERISWEATHER_API_V1_STRIP_HTTP_RESPONSE_CONTENT"] = val
        client = aeris_api_client("client_id", "client_secret")

        assert client.airquality.strip_http_response_content is False

    @pytest.mark.parametrize("val", ["1000", "tf", "yea, no"])
    def test_strip_http_response_content_invalid_value(self, val: str) -> None:
        """
        Tests that the :py:class:`AerisApiClient` is configured to strip HTTP
        response content when the required environment variable is set to
        an invalid value.
        """
        environ["AERISWEATHER_API_V1_STRIP_HTTP_RESPONSE_CONTENT"] = val
        client = aeris_api_client("client_id", "client_secret")

        assert client.airquality.strip_http_response_content is True

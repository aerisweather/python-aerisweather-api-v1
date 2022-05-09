"""
tests/model/test_response
-----------------------

Tests functionality in the aerisweather_api_v1.model.response module.
"""

from http import HTTPStatus

import pytest
import requests

from aerisweather_api_v1.model.airquality import AirQuality
from aerisweather_api_v1.model.response import AerisApiResponse, AerisApiResponseError

from testhelper.requests import make_response


@pytest.fixture
def http_response() -> requests.Response:
    return make_response(None, HTTPStatus.OK, None)


class TestAerisApiResponseError:
    """
    Tests the functionality of the :py:class:`AerisApiResponseError` object.
    """

    def test_eq_same_error(self) -> None:
        """
        Tests that a :py:class:`AerisApiResponseError` object is equal to itself.
        """
        err = AerisApiResponseError(
            "warn_no_data", "Valid request. No results available based on your query parameters."
        )

        assert err == err

    def test_eq_equivalent_errors(self) -> None:
        """
        Tests that two equivalent :py:class:`AerisApiResponseError` objects are equal.
        """
        e1 = AerisApiResponseError(
            "warn_no_data", "Valid request. No results available based on your query parameters."
        )
        e2 = AerisApiResponseError(
            "warn_no_data", "Valid request. No results available based on your query parameters."
        )

        assert e1 == e2

    def test_not_eq_error_other_object(self) -> None:
        """
        Tests that an object of a different type is not equal to a :py:class:`AerisApiResponseError`.
        """
        err = AerisApiResponseError(
            "warn_no_data", "Valid request. No results available based on your query parameters."
        )

        assert err != object()

    def test_not_eq_nonequivalent_errors(self) -> None:
        """
        Tests that two non-equivalent :py:class:`AerisApiResponseError` objects are not equal.
        """
        e1 = AerisApiResponseError(
            "warn_no_data", "Valid request. No results available based on your query parameters."
        )
        e2 = AerisApiResponseError("invalid_client", 'A valid "client_id" and "client_secret" were not provided.')

        assert e1 != e2

    def test_error_repr_is_str(self) -> None:
        """
        Tests that :py:meth:`AerisApiResponseError.__repr__` returns a string.
        """
        err = AerisApiResponseError(
            "warn_no_data", "Valid request. No results available based on your query parameters."
        )

        assert isinstance(err.__repr__(), str)


class TestAerisApiResponse:
    """
    Tests the functionality of the :py:class:`AerisApiResponse` object.
    """

    def test_eq_same_response(self, http_response: requests.Response) -> None:
        """
        Tests that a :py:class:`AerisApiResponse` object is equal to itself.
        """
        resp: AerisApiResponse[AirQuality] = AerisApiResponse(http_response, True, None, list())

        assert resp == resp

    def test_eq_equivalent_responses(self, http_response: requests.Response) -> None:
        """
        Tests that two equivalent :py:class:`AerisApiResponse` objects are equal.
        """
        r1: AerisApiResponse[AirQuality] = AerisApiResponse(http_response, True, None, list())
        r2: AerisApiResponse[AirQuality] = AerisApiResponse(http_response, True, None, list())

        assert r1 == r2

    def test_not_eq_response_other_object(self, http_response: requests.Response) -> None:
        """
        Tests that an object of a different type is not equal to a :py:class:`AerisApiResponse`.
        """
        resp: AerisApiResponse[AirQuality] = AerisApiResponse(http_response, True, None, list())

        assert resp != object()

    def test_not_eq_nonequivalent_responses(self, http_response: requests.Response) -> None:
        """
        Tests that two non-equivalent :py:class:`AerisApiResponse` objects are not equal.
        """
        r1: AerisApiResponse[AirQuality] = AerisApiResponse(http_response, True, None, list())
        r2: AerisApiResponse[AirQuality] = AerisApiResponse(
            make_response(None, HTTPStatus.BAD_REQUEST, None),
            False,
            AerisApiResponseError("bad_request", "The request was invalid."),
            list(),
        )

        assert r1 != r2

    def test_response_repr_is_str(self, http_response: requests.Response) -> None:
        """
        Tests that :py:meth:`AerisApiResponse.__repr__` returns a string.
        """
        resp: AerisApiResponse[AirQuality] = AerisApiResponse(http_response, True, None, list())

        assert isinstance(resp.__repr__(), str)

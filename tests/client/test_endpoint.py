"""
tests/client/test_endpoint
--------------------------

Tests functionality in the aerisweather_api_v1.client.endpoint module.
"""

from http import HTTPStatus
import json
from typing import Any, Dict, List, Optional

import pytest

from aerisweather_api_v1.model.common import ApiModel
from aerisweather_api_v1.model.response import AerisApiResponse
from aerisweather_api_v1.client.http import AerisApiHttpClient
from aerisweather_api_v1.client.endpoint import AerisApiEndpoint

from testhelper.requests import MockSession


class MockModel(ApiModel):
    """
    Mock model to test the base functionality of the :py:class:`AerisApiEndpoint`.

    :param temp: mock temperature value
    :param wind_speed: mock wind speed value
    :param wind_dir: mock wind direction value (in degrees, 0 - 360)
    """

    def __init__(self, temp: float, wind_speed: float, wind_dir: int) -> None:
        self.temp = temp
        self.wind_speed = wind_speed
        self.wind_dir = wind_dir


def deserialize_mock_model(o: Dict[str, Any]) -> MockModel:
    """
    Deserializes a dictionary representing :py:class:`MockModel`.

    :param o: the dictionary representation of :py:class:`MockModel`.
    """
    # The dictionary representation should look something like:
    #
    # {
    #    "temp": 70,
    #    "wind_speed": 5.8,
    #    "wind_dir":   120,
    # }
    return MockModel(o["temp"], o["wind_speed"], o["wind_dir"])


class MockAerisApiEndpoint(AerisApiEndpoint[MockModel]):
    path = "mock"
    docs = "mock"

    def id(self, id: str, fields: Optional[List[str]] = None) -> AerisApiResponse[MockModel]:
        """
        Mock :id endpoint.
        """
        query_params = self._prepare_params(locals())
        return self._request("GET", id, query_params)

    __call__ = id

    def within(self, p: Optional[str] = None, fields: Optional[List[str]] = None) -> AerisApiResponse[MockModel]:
        """
        Mock within endpoint.
        """
        query_params = self._prepare_params(locals())
        return self._request("GET", "within", query_params)


@pytest.fixture
def requests_session() -> MockSession:
    return MockSession()


@pytest.fixture
def http_client(requests_session: MockSession) -> AerisApiHttpClient:
    return AerisApiHttpClient(
        "test_endpoint_client_id",
        "test_endpoint_client_secret",
        base_url="http://localhost:3333",
        requests_session=requests_session,
    )


@pytest.fixture
def mock_endpoint(http_client: AerisApiHttpClient) -> MockAerisApiEndpoint:
    """
    Fixture that initializes and returns a :py:class:`MockAerisApiEndpoint`.
    """
    return MockAerisApiEndpoint(http_client, deserialize_mock_model)


class TestAerisApiEndpoint:
    """
    Tests the functionality of the :py:class:`AerisApiEndpoint` superclass.
    """

    def test_instantiating_unconfigured_docs_endpoint(self, http_client: AerisApiHttpClient) -> None:
        """
        Tests that instantiating an AerisApiEndpoint without docs configured raises a TypeError.
        """

        class AerisApiNoDocsEndpoint(AerisApiEndpoint[ApiModel]):
            path = "mock/path"

        with pytest.raises(TypeError):
            AerisApiNoDocsEndpoint(http_client, lambda o: ApiModel())

    def test_instantiating_unconfigured_path_endpoint(self, http_client: AerisApiHttpClient) -> None:
        """
        Tests that instantiating an AerisApiEndpoint without a path configured raises a TypeError.
        """

        class AerisApiNoPathEndpoint(AerisApiEndpoint[ApiModel]):
            docs = "https://www.aerisweather.com/docs/mock"

        with pytest.raises(TypeError):
            AerisApiNoPathEndpoint(http_client, lambda o: ApiModel())

    @pytest.mark.parametrize(
        "ep_id, temp, wind_speed, wind_dir",
        [
            ("55344", 70.5, 5.8, 270),
            ("mock1", 38.6, 2.0, None),
        ],
    )
    def test_mock_id_action(
        self,
        mock_endpoint: MockAerisApiEndpoint,
        requests_session: MockSession,
        ep_id: str,
        temp: float,
        wind_speed: float,
        wind_dir: Optional[float],
    ) -> None:
        """
        Tests the functionality of the mock :id action.
        """
        response_dict = {
            "success": True,
            "error": None,
            "response": [
                {
                    "temp": temp,
                    "wind_speed": wind_speed,
                    "wind_dir": wind_dir,
                },
            ],
        }
        requests_session.add_response(HTTPStatus.OK, json.dumps(response_dict))

        response = mock_endpoint.id(ep_id)
        m = response.api_response[0]

        assert response.http_response.status_code == HTTPStatus.OK
        assert m.temp == temp
        assert m.wind_speed == wind_speed
        assert m.wind_dir == wind_dir

    @pytest.mark.parametrize(
        "p, temp, wind_speed, wind_dir",
        [
            ("55344", 70.5, 5.8, 270),
            ("new york,ny", 38.6, 2.0, None),
        ],
    )
    def test_mock_within_action(
        self,
        mock_endpoint: MockAerisApiEndpoint,
        requests_session: MockSession,
        p: str,
        temp: float,
        wind_speed: float,
        wind_dir: Optional[float],
    ) -> None:
        """
        Tests the functionality of the mock within action.
        """
        response_dict = {
            "success": True,
            "error": None,
            "response": [
                {
                    "temp": temp,
                    "wind_speed": wind_speed,
                    "wind_dir": wind_dir,
                },
            ],
        }
        requests_session.add_response(HTTPStatus.OK, json.dumps(response_dict))

        response = mock_endpoint.within(p=p, fields=["temp", "wind_speed", "wind_dir"])

        m = response.api_response[0]

        assert response.http_response.status_code == HTTPStatus.OK
        assert m.temp == temp
        assert m.wind_speed == wind_speed
        assert m.wind_dir == wind_dir

    def test_mock_within_no_data(
        self,
        mock_endpoint: MockAerisApiEndpoint,
        requests_session: MockSession,
    ) -> None:
        """
        Tests the functionality of the mock within action when "warn_no_data" is returned.
        """
        err_code = "warn_no_data"
        err_desc = "Valid request. No results available based on your query parameters."
        response_dict = {
            "success": True,
            "error": {
                "code": err_code,
                "description": err_desc,
            },
            "response": [],
        }
        requests_session.add_response(HTTPStatus.OK, json.dumps(response_dict))

        response = mock_endpoint.within(p="55344")

        assert response.error is not None
        assert response.error.code == err_code
        assert response.error.description == err_desc
        assert response.api_response == []

    def test_response_none_converted_to_empty_list(
        self,
        mock_endpoint: MockAerisApiEndpoint,
        requests_session: MockSession,
    ) -> None:
        """
        Tests that a response value of ``None`` is converted to an empty list.
        """
        response_dict = {
            "success": True,
            "error": None,
            "response": None,
        }
        requests_session.add_response(HTTPStatus.OK, json.dumps(response_dict))

        response = mock_endpoint.within(p="55344")

        assert response.api_response == []

    def test_response_single_object_converted_to_list(
        self,
        mock_endpoint: MockAerisApiEndpoint,
        requests_session: MockSession,
    ) -> None:
        """
        Tests that a single-object (non-list) response gets converted to a list.
        """
        response_dict = {
            "success": True,
            "error": None,
            "response": {
                "temp": 65.5,
                "wind_speed": 5.5,
                "wind_dir": 180,
            },
        }
        requests_session.add_response(HTTPStatus.OK, json.dumps(response_dict))

        response = mock_endpoint.within(p="55344")

        assert isinstance(response.api_response, list)

"""
testhelper/requests
-------------------

Provides requests-related helper code for tests.
"""

from http import HTTPStatus
import json
from unittest.mock import MagicMock
from typing import Any, Dict, List, Tuple, Union

import requests


def make_response(request: requests.PreparedRequest, status_code: int, content: str) -> requests.Response:
    response = requests.Response()
    response.request = request
    response.status_code = status_code
    response._content = content.encode("utf-8")

    return response


class MockSession(requests.Session):
    def __init__(self, *args: List[Any], **kwargs: Dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)

        self._responses: List[Tuple[int, str]] = list()

        def get_response(request: requests.PreparedRequest, **kwargs: Dict[str, Any]) -> requests.Response:
            try:
                status_code, content = self._responses.pop()
            except IndexError:
                status_code, content = (HTTPStatus.OK, json.dumps({"status": "ok"}))

            return make_response(request, status_code, content)

        self.send_mock = MagicMock(side_effect=get_response)

    def add_response(self, status_code: int, body: str) -> None:
        """
        Adds a mock response to be returned by this session.

        :param status_code: the HTTP status code of the response
        :param body: the content of the response body
        """
        self._responses.append((status_code, body))

    def get_adapter(self, url: str) -> None:  # type: ignore
        """
        Mock override of :py:meth:`requests.Session.get_adapter`.

        Does nothing so that there is no inadvertent network activity.
        """

    def mount(self, prefix: Union[str, bytes], adapter: requests.adapters.BaseAdapter) -> None:
        """
        Mock override of :py:meth:`requests.Session.mount`.

        Does nothing so that there is no inadvertent network activity.
        """

    def send(self, request: requests.PreparedRequest, **kwargs: Dict[str, Any]) -> requests.Response:  # type: ignore
        """
        Mock override of :py:meth:`requests.Session.send`.

        Returns a fake response. Does not make any real requests over the network.
        """
        response = self.send_mock(request, **kwargs)
        assert isinstance(response, requests.Response)
        return response

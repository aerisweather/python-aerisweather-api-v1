"""
testhelper/requests
-------------------

Provides requests-related helper code for tests.
"""

from http import HTTPStatus
import json
from urllib.parse import urlparse, parse_qs
from unittest.mock import MagicMock
from typing import Any, List, Mapping, Optional, Tuple, Union

import requests


def make_response(
    request: Optional[requests.PreparedRequest], status_code: int, content: Optional[str]
) -> requests.Response:
    response = requests.Response()

    # When constructing the expected AerisApiResponse object during
    # endpoint/client tests, we won't have a proper PreparedRequest.
    #
    # Therefore, we allow it to be set to None here.
    response.request = request  # type: ignore

    response.status_code = status_code

    # When constructing the expected AerisApiResponse object during
    # endpoint/client tests, we do not need to provide the full content
    # of the body for comparison so allow it to be omitted.
    #
    # When the AerisApiClient is invoked, the requests.Response object
    # that is returned has content stripped to save memory.
    if content is not None:
        response._content = content.encode("utf-8")

    return response


def request_equals(
    request: requests.PreparedRequest,
    path: str,
    query: Mapping[str, str],
    body: Union[None, str, Mapping[str, Any], List[Any]],
) -> bool:
    """
    Returns ``True`` if ``request`` is matches the given ``scheme``, ``netloc``, ``path``, and
    ``query``, ``body``.

    See also :py:func:`urllib.parse.urlparse`.

    :param request: the PreparedRequest object representing the request that would have been made
    :param path: the path part of the URI
    :param query: the query parameters of the URI
    :param body: the payload sent with the request
    """
    if not _body_equal(request.body, body):
        return False

    parsed_url = urlparse(request.url)
    if isinstance(parsed_url.query, str):
        parsed_query = parse_qs(parsed_url.query)
    else:
        parsed_query = parse_qs(parsed_url.query.decode("utf-8"))

    normalized_query = dict()
    for k, v in parsed_query.items():
        if len(v) > 1:
            raise ValueError("multi-value parameters not permitted")
        normalized_query[k] = v[0]

    parsed_url_path = parsed_url.path
    assert isinstance(parsed_url_path, str)

    # body has already been verified above, so we don't need to check it again here.
    #
    # parsed_url_path and path are normalized here so we don't need to worry about
    # leading and trailing slashes.
    return parsed_url_path.strip("/") == path.strip("/") and normalized_query == query


def _body_equal(
    request_body: Union[str, bytes, None], expected_body: Union[None, str, Mapping[str, Any], List[Any]]
) -> bool:
    """
    Validates that the given ``request_body`` is equivalent to the ``expected_body``.

    This seems like it should be trivial but there is some nuance introduced by the
    fact that our request bodies contain JSON payloads.

    In the interest of tests not containing massive string literal JSON-blobs and
    allowing for the order of object keys to remain insignificant, we need to try
    parsing the ``request_body`` as JSON and comparing it to the ``expected_body``.

    :param request_body: the body of the :py:class:`requests.PreparedRequest`
    :param expected_body: a representation of the body that was expected; \
        either ``None``, a raw string, or a dictionary or list (representing a JSON payload)
    """

    # First deal with the simple case: was there a request body at all?
    #
    # For the purposes of comparison, None and empty string are the same.
    if request_body is None:
        return expected_body is None or expected_body == ""
    elif expected_body is None:
        # request_body is *not* None, but expected_body is.
        # Only an empty request_body is acceptable.
        return request_body == ""

    # At this point, request_body can be either bytes or str.
    # expected_body can be any non-None value.
    if isinstance(request_body, bytes):
        request_body = request_body.decode("utf-8")

    # At this point, request_body will always be a str.
    if isinstance(expected_body, str):
        return request_body == expected_body

    # At this point, expected_body can either a list or dict.
    # request_body is still always a str.
    #
    # The last thing to try is parsing the request_body as JSON
    # and seeing if that matches the expected_body.
    request_parsed = json.loads(request_body)

    return bool(request_parsed == expected_body)


class MockSession(requests.Session):
    def __init__(self, *args: List[Any], **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self._responses: List[Tuple[int, str]] = list()

        def get_response(request: requests.PreparedRequest, **kwargs: Any) -> requests.Response:
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

    def mount(self, prefix: Union[str, bytes], adapter: Any) -> None:
        """
        Mock override of :py:meth:`requests.Session.mount`.

        Does nothing so that there is no inadvertent network activity.
        """

    def send(self, request: requests.PreparedRequest, **kwargs: Any) -> requests.Response:
        """
        Mock override of :py:meth:`requests.Session.send`.

        Returns a fake response. Does not make any real requests over the network.
        """
        response = self.send_mock(request, **kwargs)
        assert isinstance(response, requests.Response)
        return response

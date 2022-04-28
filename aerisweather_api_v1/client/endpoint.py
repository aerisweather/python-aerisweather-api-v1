"""
aerisweather_api_v1/client/endpoint
-----------------------------------

Contains generic endpoint code for the Aeris API v1 client.
"""

import json
from typing import Any, Callable, Dict, List, Generic, Optional, Union

import requests

from ..error import InvalidAerisApiResponseError
from ..model.common import ApiModelG
from ..model.response import AerisApiResponse, AerisApiResponseError
from .http import AerisApiHttpClient


class AerisApiEndpoint(Generic[ApiModelG]):
    """
    Superclass for endpoints of the Aeris API v1.

    This class provides common endpoint functionality. All endpoints to be
    used by the AerisApiClientV1 should be a subclass of this class.

    :param http_client: the HTTP client used by the parent AerisApiClientV1 (or a copy of it)
    :param deserializer: callable that parses endpoint result and returns a model
    :param strip_http_response_content: If ``True``, strips the content from :py:class:`requests.Response` \
        objects before returning them as part of a :py:class:`AerisApiResponse`. Stripping the \
        response content can help save memory, but preserving it can be useful for debugging. \
        Defaults to ``True``
    """

    #: The URL path to this Aeris API endpoint.
    path = "undefined"

    #: The URL of the Aeris API documentation for this endpoint.
    docs = "undefined"

    def __init__(
        self,
        http_client: AerisApiHttpClient,
        deserializer: Callable[[Dict[str, Any]], ApiModelG],
        strip_http_response_content: bool = True,
    ) -> None:
        path_ok = self.__class__.path != AerisApiEndpoint.path
        docs_ok = self.__class__.docs != AerisApiEndpoint.docs

        # Design note: abstract classes provide this functionality,
        # but the syntax for subclasses kind of sucks. Rather than
        # set simple attributes at the top of a class, abstract
        # base classes require all abstract properties to actually
        # be @property decorated methods.
        if not (path_ok and docs_ok):
            raise TypeError(f"{self.__class__.__name__} is missing attributes required for endpoint")

        self.http = http_client
        self.deserializer = deserializer
        self.strip_http_response_content = strip_http_response_content

    def _prepare_param(self, k: str, v: Any) -> str:
        """
        Given an endpoint parameter ``k`` with value ``v``, prepares
        the parameter for submission to the Aeris API.

        :param k: the name of the parameter to be sent to the Aeris API
        :param v: the value of the parameter to be sent to the Aeris API
        """
        # Some of the parameters may be numerical types. Make sure everything is
        # converted to a string before returning it.
        return str(v)

    def _prepare_params(self, params: Dict[str, Any]) -> Dict[str, str]:
        """
        Given a dictionary containing potential endpoint parameters,
        (via a call to ``locals()``), prepares the parameters for submission
        to the Aeris API.

        :param params: the result of a call to ``locals()`` containing parameters to prepare
        """
        # If endpoint methods are passing the raw output of locals(), there are
        # a couple things we definitely don't want:
        #
        # self, which is the endpoint object
        # id, which is part of the path, not query parameters
        # route, which is posted data
        p = {
            k: self._prepare_param(k, v)
            for k, v in params.items()
            if v is not None and k not in ["self", "id", "route"]
        }
        return p

    def _request(
        self,
        http_method: str,
        action: Optional[str],
        query_params: Dict[str, Any],
        data: Union[List[Any], Dict[str, Any], None] = None,
    ) -> AerisApiResponse[ApiModelG]:
        """
        Makes a request against this Aeris API endpoint using the given HTTP method,
        action, and query parameters.

        :param http_method: the HTTP method to use when invoking the endpoint, i.e. "GET" or "POST"
        :param action: the endpoint action to make a request for, or the ID for :id endpoints, e.g. \
            "closest", "search", "within", "55344"
        :param query_params: the query parameters of the request
        :param data: the payload sent with the request; not valid for "GET" requests
        """
        if http_method == "GET" and data is not None:
            raise ValueError("cannot provide data payload with 'GET' request")

        path = f"{self.path}/{action}"

        if data is None:
            http_response = self.http.request(http_method, path, params=query_params)
        else:
            http_response = self.http.request(http_method, path, params=query_params, data=json.dumps(data))

        try:
            api_response = self._handle_response(http_response)
        except Exception as e:
            raise InvalidAerisApiResponseError("failed parsing Aeris API response", http_response) from e

        if http_response.status_code >= 400 or api_response.success is False:
            if api_response.error is not None:
                api_response.error.http_response = api_response.http_response
                raise api_response.error
            else:
                raise InvalidAerisApiResponseError(
                    f"got HTTP status {http_response.status_code} but response contained no error object",
                    http_response,
                )

        # Here we strip the content from the HTTP reponse before passing it back to the user.
        # Note that this happens _after_ parsing the response and potentially raising an error.
        # Errors should include the full HTTP response body so that we know what data failed parsing.
        #
        # For normal, non-error cases, responses from the Aeris API can be quite large and not worth
        # wasting memory on. The model objects from this library will already contain all of the data from those
        # responses. If we leave the HTTP response content, it will take up something like 2x the memory.
        #
        # We could simply not return the HTTP response object. However, it provides some potentially
        # useful information for end users who are interested (elapsed time for the HTTP request,
        # status code, any headers returned with the response).
        if self.strip_http_response_content:
            http_response._content = None
            http_response.close()

        return api_response

    def _handle_response(self, http_response: requests.Response) -> AerisApiResponse[ApiModelG]:
        """
        Handles the response of an Aeris API request, returning the appropriate
        :py:class:`AerisApiResponse` or raising an error, as appropriate.

        :param http_response: the HTTP response to handle
        :return: an :py:class:`AerisApiResponse` representing ``http_response``
        """
        resp_json = http_response.json()

        success = resp_json["success"]
        raw_error = resp_json["error"]
        error = None
        if raw_error is not None:
            error = AerisApiResponseError(raw_error["code"], raw_error["description"])

        raw_response = resp_json["response"]
        if raw_response is None:
            deserialized = list()
        elif isinstance(raw_response, list):
            deserialized = [self.deserializer(o) for o in raw_response]
        else:
            deserialized = [self.deserializer(raw_response)]

        return AerisApiResponse(http_response, success, error, deserialized)

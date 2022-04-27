"""
aerisweather_api_v1/client/endpoint
-----------------------------------

Contains generic endpoint code for the Aeris API v1 client.
"""

from typing import Any, Callable, Dict, Generic, Optional

from ..model.response import AerisApiResponse, AerisApiResponseError
from .http import AerisApiHttpClient
from .types import ApiModel


class AerisApiEndpoint(Generic[ApiModel]):
    """
    Superclass for endpoints of the Aeris API v1.

    This class provides common endpoint functionality. All endpoints to be
    used by the AerisApiClientV1 should be a subclass of this class.

    :param http_client: the HTTP client used by the parent AerisApiClientV1 (or a copy of it)
    :param deserializer: callable that parses endpoint result and returns a model
    """

    #: The URL path to this Aeris API endpoint.
    path = "undefined"

    #: The URL of the Aeris API documentation for this endpoint.
    docs = "undefined"

    def __init__(self, http_client: AerisApiHttpClient, deserializer: Callable[[Dict[str, Any]], ApiModel]) -> None:
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

    def _prepare_param(self, k: str, v: Any) -> str:
        """
        Given an endpoint parameter ``k`` with value ``v``, prepares
        the parameter for submission to the Aeris API.

        :param k: the name of the parameter to be sent to the Aeris API
        :param v: the value of the parameter to be sent to the Aeris API
        """
        if k == "fields":
            return ",".join(v)

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
        p = {k: self._prepare_param(k, v) for k, v in params.items() if v is not None and k not in ["self", "id"]}
        return p

    def _request(
        self, http_method: str, action: Optional[str], query_params: Dict[str, Any]
    ) -> AerisApiResponse[ApiModel]:
        """
        Makes a request against this Aeris API endpoint using the given HTTP method,
        action, and query parameters.

        :param http_method: the HTTP method to use when invoking the endpoint, i.e. "GET" or "POST"
        :param action: the endpoint action to make a request for, or the ID for :id endpoints, e.g. \
            "closest", "search", "within", "55344"
        :param query_params: the query parameters of the request
        """
        path = f"{self.path}/{action}"

        http_response = self.http.request(http_method, path, params=query_params)
        json = http_response.json()

        # Here we strip the content from the HTTP reponse before passing it back to the user.
        #
        # Responses from the Aeris API can be quite large. The model objects from this library
        # will already contain all of the data from those responses. If we leave the HTTP response
        # content, it will take up something like 2x the memory.
        #
        # We could simply not return the HTTP response object. However, it provides some potentially
        # useful information for end users who are interested (elapsed time for the HTTP request,
        # status code, any headers returned with the response).
        http_response._content = None
        http_response.close()

        success = json["success"]

        raw_error = json["error"]
        error = None
        if raw_error is not None:
            error = AerisApiResponseError(raw_error["code"], raw_error["description"])

        raw_response = json["response"]
        if raw_response is None:
            deserialized = list()
        elif isinstance(raw_response, list):
            deserialized = [self.deserializer(o) for o in raw_response]
        else:
            deserialized = [self.deserializer(raw_response)]

        return AerisApiResponse(http_response, success, error, deserialized)

"""
aerisweather_api_v1/client/http
-------------------------------

Contains HTTP client code for v1 of the Aeris API.
"""

from typing import Any, MutableMapping, Optional

import requests

from ..__version__ import user_agent


class AerisApiHttpClient:
    """
    HTTP client for v1 of the Aeris API.

    This client provides a very thin convenience wrapper around the HTTP methods
    provided by the :external+requests:doc:`requests <index>` library. You probably
    want to use the higher-level Aeris API client.

    For most use cases, only ``client_id`` and ``client_secret`` should be specified.

    :param client_id: AerisWeather client ID used to make the request; \
        you can get one by :aerissignup:`signing up for an AerisWeather API subscription <>`
    :param client_secret: AerisWeather client secret used to make the request; \
        you can get one by :aerissignup:`signing up for an AerisWeather API subscription <>`
    :param base_url: base URL against which Aeris API requests should be made; \
        this can be overridden if you have implemented a proxy for caching
    :param requests_session: :py:class:`requests.Session`-compatible object used to make HTTP requests
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        base_url: str = "https://api.aerisapi.com",
        requests_session: Optional[requests.Session] = None,
    ) -> None:
        self.base_url = base_url

        if requests_session is None:
            self._requests = requests.Session()  # pragma: nocover
        else:
            self._requests = requests_session

        self.params: MutableMapping[str, str] = dict()
        self.client_id = client_id
        self.client_secret = client_secret
        self._requests.params = self.params
        self._requests.headers.update({"User-Agent": user_agent})

    @property
    def client_id(self) -> str:
        """
        The AerisWeather client ID used in requests made by this HTTP client.
        """
        return self._client_id

    @client_id.setter
    def client_id(self, v: str) -> str:
        self._client_id = v
        self.params["client_id"] = v
        return self._client_id

    @property
    def client_secret(self) -> str:
        """
        The AerisWeather client secret used in requests made by this HTTP client.
        """
        return self._client_secret

    @client_secret.setter
    def client_secret(self, v: str) -> str:
        self._client_secret = v
        self.params["client_secret"] = v
        return self._client_secret

    def request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        r"""
        Performs an HTTP request against the Aeris API at the given path.

        :param method: HTTP method as expected by :py:meth:`requests.Session.request`.
        :param path: path to perform request against (base URL is provided via constructor).
        :param \*\*kwargs: additional keyword arguments as expected by :py:meth:`requests.Session.request`
        :returns: the resulting HTTP response
        """
        return self._requests.request(method, self._url(path), **kwargs)

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        r"""
        Performs an HTTP GET request against the given path.

        :param path: path to perform GET request against (base URL is provided via constructor)
        :param \*\*kwargs: keyword arguments as expected by :py:meth:`requests.Session.get`
        :returns: the resulting HTTP response
        """
        return self._requests.get(self._url(path), **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        r"""
        Performs an HTTP POST request against the given path.

        :param path: path to perform POST request against (base URL is provided via constructor)
        :param \*\*kwargs: keyword arguments as expected by :py:meth:`requests.Session.post`
        :returns: the resulting HTTP response
        """
        return self._requests.post(self._url(path), **kwargs)

    def _url(self, path: str) -> str:
        """
        Given a path, returns the full URL that HTTP requests should be made against.

        :param path: path against which requests should be made
        :returns: a full URL constructed from the base URL and given path
        """
        return f"{self.base_url}/{path.lstrip('/')}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(client_id={self.client_id}, base_url={self.base_url})"

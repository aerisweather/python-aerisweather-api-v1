"""
aerisweather_api_v1/error
-------------------------

Defines custom errors raised by this SDK.
"""

import requests


class AerisApiError(Exception):
    """
    Base class for all custom errors raised by this SDK.
    """


class InvalidAerisApiResponseError(AerisApiError):
    """
    Raised when an error is encountered parsing the response from the Aeris API.

    :param message: the error message associated with this exception
    :param http_response: the HTTP response that triggered this exception
    """

    def __init__(self, message: str, http_response: requests.Response) -> None:
        super().__init__(message)
        self.http_response = http_response

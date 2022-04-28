"""
aerisweather_api_v1/model/response
----------------------------------

Contains the definition for an Aeris API v1 response.
"""

from typing import Any, Generic, List, Optional, TypeVar

import requests

from ..error import AerisApiError

ApiModel = TypeVar("ApiModel")


class AerisApiResponseError(AerisApiError):
    """
    Class representing the error object of an Aeris API v1 response.

    If the error is non-recoverable, this will be raised as an exception.

    :param code: the error code
    :param message: the error message
    """

    def __init__(self, code: str, message: str) -> None:
        #: The error code.
        self.code = code

        #: The error message.
        self.description = message

        #: The HTTP response that caused this error to be raised as an exception.
        #: This will ONLY be set if this error is raised as an exception.
        self.http_response: Optional[requests.Response] = None

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if ``other`` is a :py:class:`AerisApiResponseError` with the same
        attributes as this one, otherwise returns False.

        :param other: another object
        """
        if not isinstance(other, self.__class__):
            return False

        return self.code == other.code and self.description == other.description

    def __repr__(self) -> str:
        return f"{self.code}: {self.description}"


class AerisApiResponse(Generic[ApiModel]):
    """
    Class representing an Aeris API v1 response.

    :param http_response: the raw HTTP response from the API, as returned by requests; \
        NOTE: the content of the response is normally not available; it is cleared to \
        save memory
    :param error: the error object returned as part of the API response
    :param api_response: the deserialized objects returned by the Aeris API
    """

    def __init__(
        self,
        http_response: requests.Response,
        success: bool,
        error: Optional[AerisApiResponseError],
        api_response: List[ApiModel],
    ) -> None:
        self.http_response = http_response
        self.success = success
        self.error = error
        self.api_response = api_response

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if ``other`` is a :py:class:`AerisApiResponse` with the same
        attributes as this one, otherwise returns False.

        :param other: another object
        """
        if not isinstance(other, self.__class__):
            return False

        return (
            self.http_response.status_code == other.http_response.status_code
            and self.success == other.success
            and self.error == other.error
            and self.api_response == other.api_response
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"http_response={self.http_response}, "
            f"success={self.success}, "
            f"error={self.error}, "
            f"api_response={self.api_response}"
            ")"
        )

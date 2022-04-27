"""
aerisweather_api_v1/client/types
--------------------------------

Contains type definitions used by the Aeris API v1 client.
"""

from typing import Optional, TypeVar, Union

try:
    from typing import Literal

    #: Describes allowable values for the Aeris API "format" argument.
    #: Should be one of "geojson" or "json".
    AerisApiFormat = Optional[Union[Literal["geojson"], Literal["json"]]]
except ImportError:
    AerisApiFormat = Optional[str]  # type: ignore

#: TypeVar for use with generics representing an object model class
#: defined within this library.
ApiModel = TypeVar("ApiModel")

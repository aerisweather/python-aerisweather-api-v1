"""
aerisweather_api_v1
-------------------

The aerisweather_api_v1 module implements a Python interface to the
AerisWeather API, version 1.

https://www.aerisweather.com/

(c) 2018-2022 by AerisWeather
"""

from .client import aeris_api_client
from .model.common import RouteParameterObject, RouteGeoJsonFeature
from .__version__ import __version__

__all__ = [
    "aeris_api_client",
    "RouteGeoJsonFeature",
    "RouteParameterObject",
    "__version__",
]

# flake8: noqa: F401

"""
aerisweather/__version__.py
---------------------------

Contains the current version of the AerisWeather Python SDK.
"""

from requests import __version__ as _requests_version

_module_name = __name__.split(".")[0]

try:
    from importlib.metadata import version as _v

    __version__ = _v(_module_name)
    del _v
except ImportError:
    from pkg_resources import get_distribution as _getdist

    __version__ = _getdist(_module_name).version
    del _getdist

user_agent = f"aerisweather_api_v1 {__version__} (requests {_requests_version})"

del _module_name
del _requests_version

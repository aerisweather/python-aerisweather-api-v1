"""
aerisweather_api_v1/logging
---------------------------

Contains logging helper code.
"""

import logging


def getLogger(name: str) -> logging.Logger:
    """
    Small wrapper function around ``getLogger`` to ensure all loggers are
    appropriately namespaced under ``aerisweather.api_v1``.

    :param name: the name of the logger to get
    :return: a logger of the given name, prefixed by ``aerisweather.api_v1.``
    """
    return logging.getLogger(f"aerisweather.api_v1.{name}")

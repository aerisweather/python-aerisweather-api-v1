################
Reference Manual
################

This section of the documentation provides information about the methods,
classes, and functions of the AerisWeather API v1 Python SDK.

.. module:: aerisweather_api_v1

******
Client
******

.. autofunction:: aerisweather_api_v1.client.aeris_api_client

.. autoclass:: aerisweather_api_v1.client.AerisApiClient

    :py:class:`aerisweather_api_v1.client.AerisApiClient` defines attributes that
    allow access to raw HTTP methods and endpoints for the Aeris API.

    .. autosummary::
        aerisweather_api_v1.client.airquality.AerisApiAirQualityEndpoint <airquality>

******
Models
******

This section describes the model objects defined by the SDK. These models
will be the result of a query against the Aeris API.

.. automodule:: aerisweather_api_v1.model.common
   :members:

.. automodule:: aerisweather_api_v1.model.airquality
   :members:

*******
Utility
*******

This section describes utility code within the SDK.

Logging
=======

.. autofunction:: aerisweather_api_v1.logging.getLogger

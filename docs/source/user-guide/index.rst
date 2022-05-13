==========
User Guide
==========

The user guide will help you get up to speed quickly with
the AerisWeather Python SDK.

How Do I...?
============

...use my own proxy to the Aeris API?
-------------------------------------

If you have configured a custom CloudFront distribution or other
caching proxy to reduce your requests to the Aeris API, you can
make use of it by passing ``base_url`` when you call
:py:func:`aerisweather_api_v1.client.aeris_api_client`. For
example:

.. code-block:: python

   aeris = aeris_api_client(client_id, client_secret, base_url="https://aerisproxy.example.com")


Any requests will be made against ``https://aerisproxy.example.com`` instead of
against the Aeris API directly.

.. note::
   The proxy you configure **must** preserve the path, query parameters, and body
   of the request. If the proxy is not functionally equivalent to the Aeris API,
   the SDK will not function correctly.

...make a raw HTTP request against the Aeris API?
-------------------------------------------------

After creating an :py:func:`aerisweather_api_v1.client.AerisApiClient`,
use the ``http`` attribute to perform a ``GET`` or ``POST`` request
to the Aeris API. It has the same interface as a :py:class:`requests.Session`,
except that there are some things which are implied:

* the base URL (e.g. ``https://api.aerisapi.com``) is implicit in every request
* ``client_id`` and ``client_secret`` are implicit in every request

For example, if you want to query the conditions endpoint:

.. code-block:: python

   aeris = aeris_api_client(client_id, client_secret)
   http_response = aeris.http.get("conditions/55344")

   # http_response is a requests.Response object

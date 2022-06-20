.. readme-include-start
AerisWeather API v1 Python SDK
==============================

The `AerisWeather`_ API Python SDK is the official Python interface to
AerisWeather's API (v1). The SDK is focused on simplicity, to help you get
started quickly, while remaining flexible enough to tackle an array of use
cases.

Getting Started
---------------

To make use of the AerisWeather API v1 Python SDK, you'll need:

1. Python 3.6+. **Python 2 is not supported**.
2. An `AerisWeather`_ account. Don't have one? `Sign up here`_!
3. An internet connection while you are making AerisWeather API queries.
4. The ``aerisweather[api_v1]`` package from `PyPI`_.

With a little code, you're off to the races!

.. code-block:: python

    import os
    from aerisweather_api_v1 import aeris_api_client

    # Use AerisWeather credentials from environment variables
    client_id = os.environ["AERIS_CLIENT_ID"]
    client_secret = os.environ["AERIS_CLIENT_SECRET"]

    aeris = aeris_api_client(client_id, client_secret)
    conditions_ny = aeris.conditions("New York, NY")

.. code-block:: python

    # Example Output
    conditions_ny = Response(

    )


.. _AerisWeather: https://www.aerisweather.com
.. _PyPI: https://pypi.org/
.. _Sign up here: https://www.aerisweather.com/pricing
.. readme-include-end

Ready for more? Check out the rest of the docs!

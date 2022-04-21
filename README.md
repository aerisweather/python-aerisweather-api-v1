AerisWeather Python SDK
=======================

The AerisWeather Python SDK is the official Python interface to
[AerisWeather][1]'s API offerings. The SDK is focused on simplicity,
to help you get started quickly, while remaining flexible enough
to tackle an array of use cases.

Getting Started
---------------

To make use of the AerisWeather Python SDK, you'll need:

* Python 3.6+. **Python 2 is not supported**.
* An [AerisWeather][1] account. Don't have one? [Sign up here][2]!
* An internet connection while you are making [AerisWeather][1]
  API queries.
* The `aerisweather` package from PyPI.

With a little code, you're off to the races!

    import os
    from aerisweather_api_v1 import aeris_api_client

    client_id = os.environ["AERIS_CLIENT_ID"]
    client_secret = os.environ["AERIS_CLIENT_SECRET"]

    aeris = aeris_api_client(client_id, client_secret)
    conditions_ny = aeris.conditions("New York, NY")

Ready for more? Check out our documentation.

[1]: https://www.aerisweather.com
[2]: https://www.aerisweather.com/pricing/

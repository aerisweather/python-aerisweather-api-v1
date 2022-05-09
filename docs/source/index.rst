AerisWeather API v1 Python SDK
==============================

The `AerisWeather`_ API Python SDK is the official Python interface to
AerisWeather's API (v1). The SDK is focused on simplicity, to help you get
started quickly, while remaining flexible enough to tackle an array of use
cases.

Getting Started
---------------

To make use of the AerisWeather API v1 Python SDK, you'll need:

* Python 3.6+. **Python 2 is not supported**.
* An `AerisWeather`_ account. Don't have one? `Sign up here`_!
* An internet connection while you are making AerisWeather API queries.
* The ``aerisweather[api_v1]`` package from `PyPI`_.

With a little code, you're off to the races!

.. code-block:: python

    import os
    from aerisweather_api_v1 import aeris_api_client

    client_id = os.environ["AERIS_CLIENT_ID"]
    client_secret = os.environ["AERIS_CLIENT_SECRET"]

    aeris = aeris_api_client(client_id, client_secret)
    conditions_ny = aeris.conditions("New York, NY")


..
    main table of contents for the sidebar

.. toctree::
   :maxdepth: 2
   :hidden:

   reference

User Guide
----------

The user guide is the first stop for newcomers to this SDK. Here, you'll
quickly be brought up to speed on how to accomplish the most common goals for
users of the SDK. Advanced users will learn supported ways to plug-in to the
SDK to better suit their needs. You'll also learn about the technical
philosophy on which the AerisWeather Python SDK was built.

Reference Manual
----------------

The reference manual provides information about the methods, classes, and
functions of this SDK. If you are already comfortable with how the SDK works
and you need to look up something specific, the reference manual is where you
want to be.

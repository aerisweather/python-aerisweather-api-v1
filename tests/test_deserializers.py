"""
tests/test_deserializers
------------------------

Tests functionality in the aerisweather_api_v1.deserializers module that is
not covered by the suite of endpoint tests.

For example, this module may include tests to attempt deserializing bad data,
or to ensure that the deserialization routines are sufficiently lenient
with the input data they accept.
"""

import json

import pytest

from aerisweather_api_v1.deserializers.common import _deserialize_try_geojson
from aerisweather_api_v1.deserializers.airquality import deserialize_airquality

from testhelper import load_test_data


class TestDeserializeTryGeoJson:
    """
    Tests the functionality of the :py:func:`_deserialize_try_geojson` function.
    """

    def test_missing_properties_response_raises_exception(self) -> None:
        """
        Tests that a GeoJSON response that is missing the ``response`` property
        raises a :py:class:`ValueError`. Because the ``response`` property contains
        the actual API model data, deserialization cannot continue if that property
        is missing.
        """
        data = json.loads(load_test_data("deserializers/geojson-missing-properties-response.txt"))

        for r in data["response"]:
            with pytest.raises(ValueError):
                _deserialize_try_geojson(r, deserialize_airquality)

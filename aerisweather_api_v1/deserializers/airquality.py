"""
aerisweather_api_v1/deserializers/airquality
--------------------------------------------

Contains deserialization functions that build model
objects from Aeris API v1 responses.
"""

from typing import Any, Dict

from ..model.common import Location, Place
from ..model.airquality import (
    AirQualityObservation,
    AirQualityPollutant,
    AirQualityProfile,
    AirQualitySource,
    AirQuality,
)
from ..util import JsonObjectWalker
from .common import deserialize_aeris_datetimeIso, deserialize_relativeTo


def deserialize_airquality(o: Dict[str, Any]) -> AirQuality:
    """
    Given an Aeris API air quality object, constructs the appropriate
    :py:class:`AirQuality` model.

    :param o: the object from which to construct a :py:class:`AirQuality`; \
        the structure should match the ``response`` items returned by the \
        :aerisapi_epprop:`Aeris API air quality endpoint <airquality>`.
    """
    w = JsonObjectWalker()
    w.set_object(o, AirQuality.__name__)
    location = Location(lat=w("loc", "lat"), long=w("loc", "long"))
    place = Place(name=w("place", "name"), state=w("place", "state"), country=w("place", "country"))
    periods = [deserialize_airquality_observation(i) for i in w("periods")]
    profile = deserialize_airquality_profile(w("profile"))
    relative_to = deserialize_relativeTo(o.get("relativeTo", None))

    return AirQuality(w("id"), location, place, periods, profile, relative_to)


def deserialize_airquality_observation(o: Dict[str, Any]) -> AirQualityObservation:
    """
    Given an Aeris API air quality observation object, constructs the appropriate
    :py:class:`AirQualityObservation`.

    :param o: the object from which to construct a :py:class:`AirQualityObservation`; \
        the structure should match the ``periods`` items returned by the \
        :aerisapi_epprop:`Aeris API air quality endpoint <airquality>`.
    """
    w = JsonObjectWalker()
    w.set_object(o, AirQualityObservation.__name__)
    dt = deserialize_aeris_datetimeIso(w("dateTimeISO"))
    aq_method = w("method")
    pollutants = [deserialize_airquality_pollutant(i, aq_method) for i in w("pollutants")]
    return AirQualityObservation(dt, w("aqi"), w("category"), w("color"), aq_method, w("dominant"), pollutants)


def deserialize_airquality_pollutant(o: Dict[str, Any], default_method: str) -> AirQualityPollutant:
    """
    Given an Aeris API air quality pollutant object, constructs the appropriate
    :py:class:`AirQualityPollutant`.

    :param o: the object from which to construct a :py:class:`AirQualityPollutant`; \
        the structure should match the ``pollutants`` items returned by the \
        :aerisapi_epprop:`Aeris API air quality endpoint <airquality>`.
    :param default_method: the default method to assign to a pollutant; \
        some air quality endpoints do not return "method" with the pollutant object
    """
    w = JsonObjectWalker()
    w.set_object(o, AirQualityPollutant.__name__)
    return AirQualityPollutant(
        w("type"),
        w("name"),
        w("valuePPB"),
        w("valueUGM3"),
        w("aqi"),
        w("category"),
        w("color"),
        w("method", default=default_method),
    )


def deserialize_airquality_profile(o: Dict[str, Any]) -> AirQualityProfile:
    """
    Given an Aeris API air quality profile, constructs the appropriate
    :py:class:`AirQualityProfile`.
    """
    w = JsonObjectWalker()
    w.set_object(o, AirQualityProfile.__name__)
    sources = [deserialize_airquality_source(i) for i in w("sources")]

    # The Aeris API sometimes returns a null "stations" property.
    # For consistency, turn it into an empty list.
    return AirQualityProfile(w("tz"), sources, w("stations") or [])


def deserialize_airquality_source(o: Dict[str, Any]) -> AirQualitySource:
    """
    Given an Aeris API air quality source, constructs the appropriate
    :py:class:`AirQualitySource`.
    """
    w = JsonObjectWalker()
    w.set_object(o, AirQualitySource.__name__)
    return AirQualitySource(w("name"))

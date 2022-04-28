"""
aerisweather_api_v1/deserializers/common
----------------------------------------

Contains deserialization functions for data structures
that are common between Aeris API endpoints.
"""

from datetime import datetime
from functools import partial
from typing import Any, Callable, Dict, Optional

from geojson import GeoJSON

from ..model.common import ApiModelG, ApiModelGeoJson, RelativeTo
from ..util import JsonObjectWalker


def deserialize_aeris_datetimeIso(s: str) -> datetime:
    """
    Deserializes a standard Aeris API dateTimeISO field.

    Aeris dateTimeISO fields take the form: ``2022-04-27T13:00:00-05:00``

    Python versions prior to 3.7 are unable to parse timezone offsets containing
    a ``:``, so some additional normalization logic is required.

    :param s: the dateTimeISO string as returned by the Aeris API v1
    """
    normalized_date_str = s.replace(":", "")

    return datetime.strptime(normalized_date_str, "%Y-%m-%dT%H%M%S%z")


def _deserialize_try_geojson(o: Dict[str, Any], model_deserializer: Callable[[Dict[str, Any]], ApiModelG]) -> ApiModelG:
    """
    Attempts to deserialize an Aeris API model by parsing it as a GeoJSON feature.
    If ``o`` is a valid GeoJSON feature, the content of properties.response is
    passed to ``model_deserializer`` and the GeoJSON feature is added to the resulting
    model.

    If ``o`` is not a valid GeoJSON feature, ``o`` is passed to ``model_deserializer``.

    :param o: the object to attempt to deserialize
    :param model_deserializer: callable that deserializes an Aeris API model
    """
    try:
        g: Optional[ApiModelGeoJson] = GeoJSON.to_instance(o, strict=True)

        # With strict=true, g will always be a GeoJSON. If `o` cannot
        # be converted to a valid GeoJSON, a ValueError will be raised
        # above.
        assert g is not None

        model_dict = g.properties["response"]
        del g.properties["response"]
    except KeyError:
        # o is a valid GeoJSON object, but it doesn't have the "response"
        # property we expect. "response" contains the model; we can't
        # continue without it.
        raise ValueError("GeoJSON object missing 'properties.response'")
    except ValueError:
        # `o` does not represent a GeoJSON object
        g = None
        model_dict = o

    model = model_deserializer(model_dict)
    model.geojson = g
    return model


def make_deserialize_try_geojson(
    model_deserializer: Callable[[Dict[str, Any]], ApiModelG]
) -> Callable[[Dict[str, Any]], ApiModelG]:
    """
    Creates a deserializer that attempts to unwrap the GeoJSON from an Aeris API model.
    """
    return partial(_deserialize_try_geojson, model_deserializer=model_deserializer)


def deserialize_relativeTo(o: Optional[Dict[str, Any]]) -> Optional[RelativeTo]:
    """
    Deserializes an Aeris API ``relativeTo`` object. Because ``relativeTo`` objects
    are only returned by queries against the ``closest`` action, this may return
    ``None``.

    :param o: the relativeTo object as a dictionary returned by the Aeris API v1, or ``None``
    """
    if o is None:
        return None
    w = JsonObjectWalker()
    w.set_object(o, "RelativeTo")
    return RelativeTo(w("lat"), w("long"), w("bearing"), w("bearingENG"), w("distanceKM"), w("distanceMI"))

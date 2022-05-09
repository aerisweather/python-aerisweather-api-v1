"""
aerisweather/api/v1/model/common
--------------------------------

Contains common data model definitions for the Aeris API v1.

Models here are shared between Aeris API endpoints.
"""

from typing import Any, Dict, Generator, Generic, Optional, Sequence, TypeVar, Union

from geojson import Feature, FeatureCollection, LineString, Point

from ..util import optisclose

_G = TypeVar("_G", LineString, Point)
ApiModelGeoJson = Union[Feature, FeatureCollection]


# Design note:
#
# The Aeris API doesn't actually have many attributes that are common
# to all endpoints and actions. Even `loc`, which appears in many places,
# does not appear in all outputs.
#
# GeoJSON seems to be the one thing that is supported everywhere.
class ApiModel:
    """
    Base class of an Aeris API model. All Aeris API endpoint responses
    should inherit from this base class.
    """

    def __init__(self) -> None:
        #: If the request against the Aeris API is made against the ``route``
        #: action, the Aeris API will return the data in GeoJSON format. This
        #: attribute contains the GeoJSON feature that encapsulated the model.
        self.geojson: Optional[ApiModelGeoJson] = None

    def with_geojson(self, geojson: ApiModelGeoJson) -> "ApiModel":
        """
        Returns this :py:class:`ApiModel` with the given GeoJSON set.

        This is intended to be used as a shorthand for this library's test cases.

        :param geojson: the GeoJSON to associate with this model
        :return: this object, with the ``geojson`` attribute set
        """
        self.geojson = geojson
        return self


# TypeVar for indicating Aeris API models for use with generics.
# This should not be used directly.
ApiModelG = TypeVar("ApiModelG", bound=ApiModel)


class Place:
    """
    Class describing a place returned by the Aeris API v1.

    :param name: the name of the place
    :param state: abbreviation of the state in which the place is located (e.g. "mn"), may be None
    :param country: abbreviation of the country in which the place is located country (e.g. "us")
    """

    def __init__(self, name: str, state: Optional[str], country: str) -> None:
        self.name = name
        self.state = state
        self.country = country

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if ``other`` is a :py:class:`Place` with the same
        attributes as this one, otherwise returns False.

        :param other: another object
        """
        if not isinstance(other, self.__class__):
            return False

        return self.name == other.name and self.state == other.state and self.country == other.country

    def __repr__(self) -> str:
        if self.state is not None:
            return f"{self.__class__.__name__}({self.name}, {self.state}, {self.country})"
        else:
            return f"{self.__class__.__name__}({self.name}, {self.country})"


class Location:
    """
    Class describing a location returned by the Aeris API v1.

    :param lat: the latitude of the location
    :param long: the longitude of the location
    """

    def __init__(self, lat: float, long: float) -> None:
        self.lat = lat
        self.long = long

    def _iter(self) -> Generator[float, None, None]:
        yield self.lat
        yield self.long

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if ``other`` is a :py:class:`Location` with the same
        attributes as this one, otherwise returns False.

        :param other: another object
        """
        if not isinstance(other, self.__class__):
            return False

        lat_eq = optisclose(self.lat, other.lat, rel_tol=0.001, abs_tol=0.0001)
        long_eq = optisclose(self.long, other.long, rel_tol=0.001, abs_tol=0.0001)
        return lat_eq and long_eq

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(lat={self.lat}, long={self.long})"

    def __iter__(self) -> Generator[float, None, None]:
        return self._iter()

    def __getitem__(self, i: int) -> float:
        if i == 0:
            return self.lat
        elif i == 1:
            return self.long
        elif i == -1:
            return self.long
        elif i == -2:
            return self.lat
        else:
            raise IndexError("lat/long index out of range")


# The Aeris API does not use a consistent profile object between
# endpoints, but they all seem to contain a `tz`. This will be
# used as a superclass for the profile of some endpoints.
class Profile:
    """
    Class describing a profile returned by the Aeris API v1.

    :param tz: the timezone associated with the :py:class:`loc <Location>` returned \
        with the response
    """

    def __init__(self, tz: str) -> None:
        self.tz = tz

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tz={self.tz})"

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if ``other`` is a :py:class:`Profile` with the same
        attributes as this one, otherwise returns False.

        :param other: another object
        """
        if not isinstance(other, self.__class__):
            return False

        return self.tz == other.tz


class RelativeTo:
    """
    Class describing the "relativeTo" field returned by the Aeris API v1 when using
    the "closest" (and sometimes "within") actions of an endpoint. The fields of
    this object describe the position of the observation location relative to the
    requested location.

    "Requested location" is the location that was passed with the original Aeris
    API request. For example, if ``airquality/closest?p=austin,tx`` is the request,
    then ``austin,tx`` is the "requested location".

    "Observation location" is the location that the observation data actually came
    from. Following on the previous example, if there is no air quality data available
    for Austin, TX the data may come from a suburb of Austin, for example.

    :param lat: the latitude of the requested location
    :param long: the longitude of the requested location
    :param bearing: bearing in degrees of the observation location relative to requested location
    :param bearingENG: cardinal direction of observation location relative to requested location
    :param distanceKM: distance of the observation location from the requested location, in kilometers
    :param distanceMI: distance of the observation location from the requested location, in miles
    """

    def __init__(
        self,
        lat: float,
        long: float,
        bearing: int,
        bearingENG: str,
        distanceKM: float,
        distanceMI: float,
    ) -> None:
        self.lat = lat
        self.long = long
        self.bearing = bearing
        self.bearingENG = bearingENG
        self.distanceKM = distanceKM
        self.distanceMI = distanceMI

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if ``other`` is a :py:class:`RelativeTo` with the same
        attributes as this one, otherwise returns False.

        :param other: another object
        """
        if not isinstance(other, self.__class__):
            return False

        return (
            optisclose(self.lat, other.lat)
            and optisclose(self.long, other.long)
            and optisclose(self.distanceKM, other.distanceKM)
            and optisclose(self.distanceMI, other.distanceMI)
            and self.bearing == other.bearing
            and self.bearingENG == other.bearingENG
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"lat={self.lat}, "
            f"long={self.long}, "
            f"bearing={self.bearing}/{self.bearingENG}, "
            f"distanceKM={self.distanceKM}, "
            f"distanceMI={self.distanceMI}"
            ")"
        )


class RoutePlace:
    """
    Class representing a place that may be passed to the Aeris API v1's ``route``
    action.

    See the :aerisapi:`Aeris API route documentation <reference/actions/route>`.
    """

    def __init__(self, id: Optional[str], from_: Optional[str]) -> None:
        self.id = id
        self.from_ = from_

    def as_dict(self) -> Dict[str, Any]:
        raise NotImplementedError("subclasses must implement as_dict()")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, from={self.from_})"


class RouteParameterObject(RoutePlace):
    """
    Class representing a parameter object that may be passed to the Aeris API v1's
    ``route`` action.

    See the :aerisapi:`Aeris API route documentation <reference/actions/route>`.

    :param p: a string describing the place; see the :aerisapi:`places documentation <reference/places>`.
    :param id: the ID of the GeoJSON feature in the returned route output
    :param from_: the time period of interest for this particular feature
    """

    def __init__(self, p: str, id: Optional[str] = None, from_: Optional[str] = None) -> None:
        super().__init__(id, from_)

        self.p = p

    def as_dict(self) -> Dict[str, Any]:
        d = {
            "p": self.p,
        }
        if self.id is not None:
            d["id"] = self.id
        if self.from_ is not None:
            d["from"] = self.from_
        return d

    def __repr__(self) -> str:
        arg_l = list()
        if self.id is not None:
            arg_l.append(f"id={self.id}")
        arg_l.append(f"p={self.p}")
        if self.from_ is not None:
            arg_l.append(f"from={self.from_}")
        args = ", ".join(arg_l)
        return f"{self.__class__.__name__}({args})"


class RouteGeoJsonFeature(Generic[_G], RoutePlace):
    """
    Class representing a GeoJSON feature that may be passed to the Aeris API v1's
    ``route`` action.

    See the :aerisapi:`Aeris API route documentation <reference/actions/route>`.

    :param geojson: the GeoJSON feature; must be a :py:class:`Point` or :py:class:`LineString`; \
        note GeoJSON features specify (longitude, latitude) pairs **NOT** (latitude, longitude)
    :param id: the ID of the GeoJSON feature in the returned route output
    :param from_: the time period of interest for this particular feature
    """

    def __init__(self, geojson: _G, id: Optional[str] = None, from_: Optional[str] = None) -> None:
        RoutePlace.__init__(self, id, from_)

        self.geojson = geojson

    def as_dict(self) -> Dict[str, Any]:
        return self.__geo_interface__

    def __repr__(self) -> str:
        arg_l = list()
        if self.id is not None:
            arg_l.append(f"id={self.id}")
        arg_l.append(f"geojson={self.geojson}")
        if self.from_ is not None:
            arg_l.append(f"from={self.from_}")
        args = ", ".join(arg_l)
        return f"{self.__class__.__name__}({args})"

    @property
    def __geo_interface__(self) -> Dict[str, Any]:
        d = {"type": "Feature", "geometry": self.geojson.__geo_interface__}
        if self.id is not None:
            d["id"] = self.id
        if self.from_ is not None:
            props = dict()
            props["from"] = self.from_
            d["properties"] = props
        return d


Route = Sequence[RoutePlace]

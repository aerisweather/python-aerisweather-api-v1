"""
tests/model/test_common
-----------------------

Tests functionality in the aerisweather_api_v1.model.common module.
"""

from math import isclose
from typing import Any, Dict, Optional

from geojson import Point
import pytest

from aerisweather_api_v1.model.common import (
    Location,
    Place,
    Profile,
    RelativeTo,
    RouteGeoJsonFeature,
    RouteParameterObject,
    RoutePlace,
)


class TestPlace:
    """
    Tests the functionality of the :py:class:`Place` object.
    """

    def test_eq_same_place(self) -> None:
        """
        Tests that a :py:class:`Place` object is equal to itself.
        """
        p = Place("minneapolis", "mn", "us")
        assert p == p

    def test_eq_equivalent_places(self) -> None:
        """
        Tests that two equivalent :py:class:`Place` objects are equal.
        """
        assert Place("minneapolis", "mn", "us") == Place("minneapolis", "mn", "us")

    def test_not_eq_place_other_object(self) -> None:
        """
        Tests that an object of a different type is not equal to a :py:class:`Place`.
        """
        assert Place("minneapolis", "mn", "us") != object()

    def test_not_eq_nonequivalent_places(self) -> None:
        """
        Tests that two non-equivalent :py:class:`Place` objects are not equal.
        """
        # different name
        assert Place("minneapolis", "mn", "us") != Place("duluth", "mn", "us")

        # different state
        assert Place("minneapolis", "mn", "us") != Place("minneapolis", "ks", "us")

        # different country
        assert Place("minneapolis", "mn", "us") != Place("minneapolis", "mn", "ca")

    def test_place_repr_is_str(self) -> None:
        """
        Tests that :py:meth:`Place.__repr__` returns a string.
        """
        assert isinstance(Place("minneapolis", "mn", "us").__repr__(), str)
        assert isinstance(Place("minneapolis", None, "us").__repr__(), str)


class TestLocation:
    """
    Tests the functionality of the :py:class:`Location` object.
    """

    def test_eq_same_location(self) -> None:
        """
        Tests that a :py:class:`Location` object is equal to itself.
        """
        loc = Location(44.90, -93.20)

        assert loc == loc

    def test_eq_equivalent_locations(self) -> None:
        """
        Tests that two equivalent :py:class:`Location` objects are equal.
        """
        assert Location(44.90, -93.20) == Location(44.90, -93.20)

    def test_not_eq_location_other_object(self) -> None:
        """
        Tests that an object of a different type is not equal to a :py:class:`Location`.
        """
        assert Location(44.90, -93.20) != object()

    def test_not_eq_nonequivalent_locations(self) -> None:
        """
        Tests that two non-equivalent :py:class:`Location` objects are not equal.
        """
        assert Location(44.90, -93.20) != Location(43.00, -93.20)
        assert Location(44.90, -93.20) != Location(44.90, -92.00)

    def test_location_repr_is_str(self) -> None:
        """
        Tests that :py:meth:`Location.__repr__` returns a string.
        """
        assert isinstance(Location(44.90, -93.20).__repr__(), str)

    def test_location_iteration(self) -> None:
        """
        Tests the iteration functionality of a :py:class:`Location`.
        """
        lat = 44.90
        long = -93.20
        lat_long_l = list(Location(lat, long))

        assert isclose(lat_long_l[0], lat)
        assert isclose(lat_long_l[1], long)

    def test_location_getitem(self) -> None:
        """
        Tests the __getitem__ functionality of a :py:class:`Location`.
        """
        lat = 44.90
        long = -93.20

        loc = Location(lat, long)

        assert loc[0] == lat
        assert loc[1] == long

        assert loc[-1] == long
        assert loc[-2] == lat

        with pytest.raises(IndexError):
            loc[2]

        with pytest.raises(IndexError):
            loc[-3]


class TestProfile:
    """
    Tests the functionality of the :py:class:`Profile` object.
    """

    def test_profile_repr_is_str(self) -> None:
        """
        Tests that :py:meth:`Profile.__repr__` returns a string.
        """
        p = Profile(tz="America/Chicago")

        assert isinstance(p.__repr__(), str)

    def test_eq_equivalent_profile(self) -> None:
        """
        Tests that two equivalent :py:class:`Profile` objects are equal.
        """
        assert Profile(tz="America/Chicago") == Profile(tz="America/Chicago")

    def test_not_eq_profile_other_object(self) -> None:
        """
        Tests that an object of a different type is not equal to a :py:class:`Profile`.
        """
        assert Profile(tz="America/Chicago") != object()

    def test_not_eq_nonequivalent_profiles(self) -> None:
        """
        Tests that two non-equivalent :py:class:`Profile` objects are not equal.
        """
        assert Profile(tz="America/Chicago") != Profile(tz="America/New_York")


class TestRelativeTo:
    """
    Tests the functionality of the :py:class:`RelativeTo` object.
    """

    def test_relativeto_repr_is_str(self) -> None:
        """
        Tests that :py:meth:`RelativeTo.__repr__` returns a string.
        """
        r = RelativeTo(44.90, -93.20, 0, "N", 1.609, 1.0)

        assert isinstance(r.__repr__(), str)

    def test_eq_same_relativeto(self) -> None:
        """
        Tests that a :py:class:`RelativeTo` object is equal to itself.
        """
        r = RelativeTo(44.90, -93.20, 0, "N", 1.609, 1.0)
        assert r == r

    def test_eq_equivalent_relativeto(self) -> None:
        """
        Tests that two equivalent :py:class:`RelativeTo` objects are equal.
        """
        assert RelativeTo(44.90, -93.20, 0, "N", 1.609, 1.0) == RelativeTo(44.90, -93.20, 0, "N", 1.609, 1.0)

    def test_not_eq_relativeto_other_object(self) -> None:
        """
        Tests that an object of a different type is not equal to a :py:class:`RelativeTo`.
        """
        assert RelativeTo(44.90, -93.20, 0, "N", 1.609, 1.0) != object()

    def test_not_eq_nonequivalent_relativeto(self) -> None:
        """
        Tests that two non-equivalent :py:class:`RelativeTo` objects are not equal.
        """
        ref = RelativeTo(44.90, -93.20, 0, "N", 1.609, 1.0)

        assert ref != RelativeTo(44.90, -92.00, 0, "N", 1.609, 1.0)
        assert ref != RelativeTo(43.00, -93.20, 0, "N", 1.609, 1.0)
        assert ref != RelativeTo(44.90, -93.20, 180, "S", 1.609, 1.0)
        assert ref != RelativeTo(44.90, -93.20, 0, "N", 3.218, 2.0)


class TestRoutePlace:
    """
    Tests the functionality of the :py:class:`RoutePlace` object.
    """

    def test_routeplace_as_dict_raises_error(self) -> None:
        """
        Tests that :py:meth:`RoutePlace.as_dict` raises a :py:class:`NotImplementedError`.
        """
        with pytest.raises(NotImplementedError):
            RoutePlace("test_place", "+60minutes").as_dict()

    def test_route_place_repr_is_str(self) -> None:
        """
        Tests that :py:meth:`RoutePlace.__repr__` returns a string.
        """
        assert isinstance(RoutePlace("id", "+30minutes").__repr__(), str)


class TestRouteParameterObject:
    """
    Tests the functionality of the :py:class:`RouteParameterObject` object.
    """

    @pytest.mark.parametrize(
        "p, id, from_, expected_dict",
        [
            ("minneapolis,mn", "mpls", "+60minutes", {"p": "minneapolis,mn", "id": "mpls", "from": "+60minutes"}),
            ("duluth,mn", None, None, {"p": "duluth,mn"}),
        ],
    )
    def test_route_parameter_as_dict(
        self, p: str, id: Optional[str], from_: Optional[str], expected_dict: Dict[str, str]
    ) -> None:
        """
        Tests that :py:meth:`RouteParameterObject.as_dict` returns an appropriate dictionary.
        """
        assert RouteParameterObject(p=p, id=id, from_=from_).as_dict() == expected_dict

    def test_route_parameter_repr_is_str(self) -> None:
        """
        Tests that :py:meth:`RouteParameterObject.__repr__` returns a string.
        """
        assert isinstance(RouteParameterObject("minneapolis,mn", id="mpls", from_="+2hours").__repr__(), str)


class TestRouteGeoJsonFeature:
    """
    Tests the functionality of the :py:class:`RouteGeoJsonFeature` object.
    """

    @pytest.mark.parametrize(
        "geojson, id, from_, expected_dict",
        [
            (
                Point((-93.20, 44.90)),
                "mpls",
                "+60minutes",
                {
                    "type": "Feature",
                    "geometry": Point((-93.20, 44.90)).__geo_interface__,
                    "id": "mpls",
                    "properties": {"from": "+60minutes"},
                },
            )
        ],
    )
    def test_route_geojson_feature_as_dict(
        self, geojson: Any, id: Optional[str], from_: Optional[str], expected_dict: Dict[str, Any]
    ) -> None:
        assert RouteGeoJsonFeature(geojson, id, from_).as_dict() == expected_dict

    @pytest.mark.parametrize(
        "geojson, id, from_",
        [
            (
                Point((-93.20, 44.90)),
                "mpls",
                "+60minutes",
            ),
        ],
    )
    def test_route_geo_json_feature_repr_is_str(self, geojson: Any, id: str, from_: str) -> None:
        """
        Tests that :py:meth:`RouteGeoJsonFeature.__repr__` returns a string.
        """
        assert isinstance(RouteGeoJsonFeature(geojson, id, from_).__repr__(), str)

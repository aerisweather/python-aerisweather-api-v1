"""
tests/model/test_model_airquality
---------------------------------

Tests functionality in the aerisweather_api_v1.model.airquality module.
"""

from datetime import datetime

from aerisweather_api_v1.model.common import Location, Place
from aerisweather_api_v1.model.airquality import (
    AirQuality,
    AirQualityObservation,
    AirQualityPollutant,
    AirQualityProfile,
    AirQualitySource,
)


class TestAirQualityPollutant:
    """
    Tests the functionality of the :py:class:`AirQualityPollutant` object.
    """

    def test_eq_same_pollutant(self) -> None:
        """
        Tests that a :py:class:`AirQualityPollutant` object is equal to itself.
        """
        p = AirQualityPollutant(
            type="co",
            name="carbon monoxide",
            valuePPB=132.7919,
            valueUGM3=152.1896,
            aqi=1,
            category="good",
            color="00E400",
            method="airnow",
        )
        assert p == p

    def test_eq_equivalent_pollutants(self) -> None:
        """
        Tests that two equivalent :py:class:`AirQualityPollutant` objects are equal.
        """
        p1 = AirQualityPollutant(
            type="co",
            name="carbon monoxide",
            valuePPB=132.7919,
            valueUGM3=152.1896,
            aqi=1,
            category="good",
            color="00E400",
            method="airnow",
        )
        p2 = AirQualityPollutant(
            type="co",
            name="carbon monoxide",
            valuePPB=132.7919,
            valueUGM3=152.1896,
            aqi=1,
            category="good",
            color="00E400",
            method="airnow",
        )
        assert p1 == p2

    def test_not_eq_pollutant_other_object(self) -> None:
        """
        Tests that an object of a different type is not equal to a :py:class:`AirQualityPollutant`.
        """
        p = AirQualityPollutant(
            type="co",
            name="carbon monoxide",
            valuePPB=132.7919,
            valueUGM3=152.1896,
            aqi=1,
            category="good",
            color="00E400",
            method="airnow",
        )
        assert p != object()

    def test_not_eq_nonequivalent_pollutants(self) -> None:
        """
        Tests that two non-equivalent :py:class:`AirQualityPollutant` objects are not equal.
        """
        p1 = AirQualityPollutant(
            type="co",
            name="carbon monoxide",
            valuePPB=132.7919,
            valueUGM3=152.1896,
            aqi=1,
            category="good",
            color="00E400",
            method="airnow",
        )
        p2 = AirQualityPollutant(
            type="no2",
            name="nitrogen dioxide",
            valuePPB=4.159,
            valueUGM3=8.6256,
            aqi=4,
            category="good",
            color="00E400",
            method="airnow",
        )
        assert p1 != p2

    def test_pollutant_repr_is_str(self) -> None:
        """
        Tests that :py:meth:`AirQualityPollutant.__repr__` returns a string.
        """
        p1 = AirQualityPollutant(
            type="co",
            name="carbon monoxide",
            valuePPB=132.7919,
            valueUGM3=None,
            aqi=1,
            category="good",
            color="00E400",
            method="airnow",
        )
        p2 = AirQualityPollutant(
            type="co",
            name="carbon monoxide",
            valuePPB=None,
            valueUGM3=152.1896,
            aqi=1,
            category="good",
            color="00E400",
            method="airnow",
        )

        assert isinstance(p1.__repr__(), str)
        assert isinstance(p2.__repr__(), str)


class TestAirQualityObservation:
    """
    Tests the functionality of the :py:class:`AirQualityObservation` object.
    """

    def test_eq_same_observation(self) -> None:
        """
        Tests that a :py:class:`AirQualityObservation` object is equal to itself.
        """
        o = AirQualityObservation(
            dt=datetime(year=2022, month=5, day=13, hour=13, minute=0, second=0),
            aqi=20,
            category="good",
            color="00E400",
            method="airnow",
            dominant="o3",
            pollutants=[
                AirQualityPollutant(
                    type="o3",
                    name="ozone",
                    valuePPB=22.0556,
                    valueUGM3=44.1338,
                    aqi=20,
                    category="good",
                    color="00E400",
                    method="airnow",
                )
            ],
        )
        assert o == o

    def test_eq_equivalent_observations(self) -> None:
        """
        Tests that two equivalent :py:class:`AirQualityObservation` objects are equal.
        """
        o1 = AirQualityObservation(
            dt=datetime(year=2022, month=5, day=13, hour=13, minute=0, second=0),
            aqi=20,
            category="good",
            color="00E400",
            method="airnow",
            dominant="o3",
            pollutants=[
                AirQualityPollutant(
                    type="o3",
                    name="ozone",
                    valuePPB=22.0556,
                    valueUGM3=44.1338,
                    aqi=20,
                    category="good",
                    color="00E400",
                    method="airnow",
                )
            ],
        )
        o2 = AirQualityObservation(
            dt=datetime(year=2022, month=5, day=13, hour=13, minute=0, second=0),
            aqi=20,
            category="good",
            color="00E400",
            method="airnow",
            dominant="o3",
            pollutants=[
                AirQualityPollutant(
                    type="o3",
                    name="ozone",
                    valuePPB=22.0556,
                    valueUGM3=44.1338,
                    aqi=20,
                    category="good",
                    color="00E400",
                    method="airnow",
                )
            ],
        )
        assert o1 == o2

    def test_not_eq_observation_other_object(self) -> None:
        """
        Tests that an object of a different type is not equal to a :py:class:`AirQualityObservation`.
        """
        o = AirQualityObservation(
            dt=datetime(year=2022, month=5, day=13, hour=13, minute=0, second=0),
            aqi=20,
            category="good",
            color="00E400",
            method="airnow",
            dominant="o3",
            pollutants=[
                AirQualityPollutant(
                    type="o3",
                    name="ozone",
                    valuePPB=22.0556,
                    valueUGM3=44.1338,
                    aqi=20,
                    category="good",
                    color="00E400",
                    method="airnow",
                )
            ],
        )
        assert o != object()

    def test_not_eq_nonequivalent_observations(self) -> None:
        """
        Tests that two non-equivalent :py:class:`AirQualityObservation` objects are not equal.
        """
        o1 = AirQualityObservation(
            dt=datetime(year=2022, month=5, day=13, hour=13, minute=0, second=0),
            aqi=20,
            category="good",
            color="00E400",
            method="airnow",
            dominant="o3",
            pollutants=[
                AirQualityPollutant(
                    type="o3",
                    name="ozone",
                    valuePPB=22.0556,
                    valueUGM3=44.1338,
                    aqi=20,
                    category="good",
                    color="00E400",
                    method="airnow",
                )
            ],
        )
        o2 = AirQualityObservation(
            dt=datetime(year=2022, month=5, day=13, hour=13, minute=0, second=0),
            aqi=20,
            category="good",
            color="00E400",
            method="airnow",
            dominant="so2",
            pollutants=[
                AirQualityPollutant(
                    type="so2",
                    name="sulfur dioxide",
                    valuePPB=0,
                    valueUGM3=0,
                    aqi=0,
                    category="good",
                    color="00E400",
                    method="airnow",
                )
            ],
        )
        assert o1 != o2

    def test_observation_repr_is_str(self) -> None:
        """
        Tests that :py:meth:`AirQualityObservation.__repr__` returns a string.
        """
        o = AirQualityObservation(
            dt=datetime(year=2022, month=5, day=13, hour=13, minute=0, second=0),
            aqi=20,
            category="good",
            color="00E400",
            method="airnow",
            dominant="o3",
            pollutants=[
                AirQualityPollutant(
                    type="o3",
                    name="ozone",
                    valuePPB=22.0556,
                    valueUGM3=44.1338,
                    aqi=20,
                    category="good",
                    color="00E400",
                    method="airnow",
                )
            ],
        )

        assert isinstance(o.__repr__(), str)


class TestAirQualitySource:
    """
    Tests the functionality of the :py:class:`AirQualitySource` object.
    """

    def test_eq_same_source(self) -> None:
        """
        Tests that a :py:class:`AirQualitySource` object is equal to itself.
        """
        src = AirQualitySource(name="AirNow (EPA)")

        assert src == src

    def test_eq_equivalent_sources(self) -> None:
        """
        Tests that two equivalent :py:class:`AirQualitySource` objects are equal.
        """
        assert AirQualitySource(name="AirNow (EPA)") == AirQualitySource(name="AirNow (EPA)")

    def test_not_eq_source_other_object(self) -> None:
        """
        Tests that an object of a different type is not equal to a :py:class:`AirQualitySource`.
        """
        assert AirQualitySource(name="AirNow (EPA)") != object()

    def test_not_eq_nonequivalent_sources(self) -> None:
        """
        Tests that two non-equivalent :py:class:`AirQualitySource` objects are not equal.
        """
        src1 = AirQualitySource(name="AirNow (EPA)")
        src2 = AirQualitySource(name="OpenAQ")

        assert src1 != src2

    def test_source_repr_is_str(self) -> None:
        """
        Tests that :py:meth:`AirQualitySource.__repr__` returns a string.
        """
        src = AirQualitySource(name="AirNow (EPA)")

        assert isinstance(src.__repr__(), str)


class TestAirQualityProfile:
    """
    Tests the functionality of the :py:class:`AirQualityProfile` object.
    """

    def test_eq_same_profile(self) -> None:
        """
        Tests that a :py:class:`AirQualityProfile` object is equal to itself.
        """
        p = AirQualityProfile(
            tz="America/Chicago", sources=[AirQualitySource(name="AirNow (EPA)")], stations=["AIRNOW_271390505"]
        )

        assert p == p

    def test_eq_equivalent_profiles(self) -> None:
        """
        Tests that two equivalent :py:class:`AirQualityProfile` objects are equal.
        """
        p1 = AirQualityProfile(
            tz="America/Chicago", sources=[AirQualitySource(name="AirNow (EPA)")], stations=["AIRNOW_271390505"]
        )
        p2 = AirQualityProfile(
            tz="America/Chicago", sources=[AirQualitySource(name="AirNow (EPA)")], stations=["AIRNOW_271390505"]
        )

        assert p1 == p2

    def test_not_eq_profile_other_object(self) -> None:
        """
        Tests that an object of a different type is not equal to a :py:class:`AirQualityProfile`.
        """
        p = AirQualityProfile(
            tz="America/Chicago",
            sources=[AirQualitySource(name="AirNow (EPA)")],
            stations=["AIRNOW_271390505"],
        )

        assert p != object()

    def test_not_eq_nonequivalent_profiles(self) -> None:
        """
        Tests that two non-equivalent :py:class:`AirQualityProfile` objects are not equal.
        """
        p1 = AirQualityProfile(
            tz="America/Chicago",
            sources=[AirQualitySource(name="AirNow (EPA)")],
            stations=["AIRNOW_271390505"],
        )
        p2 = AirQualityProfile(
            tz="America/Chicago",
            sources=[AirQualitySource(name="OpenAQ")],
            stations=["OPENAQ_US03FC368"],
        )

        assert p1 != p2

    def test_profile_repr_is_str(self) -> None:
        """
        Tests that :py:meth:`AirQualityProfile.__repr__` returns a string.
        """
        p = AirQualityProfile(
            tz="America/Chicago",
            sources=[AirQualitySource(name="AirNow (EPA)")],
            stations=["AIRNOW_271390505"],
        )

        assert isinstance(p.__repr__(), str)


class TestAirQuality:
    """
    Tests the functionality of the :py:class:`AirQuality` object.
    """

    def test_eq_same_airquality(self) -> None:
        """
        Tests that a :py:class:`AirQuality` object is equal to itself.
        """
        aq = AirQuality(
            id=None,
            loc=Location(lat=44.85469, long=-93.47079),
            place=Place(name="eden prairie", state="mn", country="us"),
            periods=[
                AirQualityObservation(
                    dt=datetime(year=2022, month=5, day=13, hour=13, minute=0, second=0),
                    aqi=20,
                    category="good",
                    color="00E400",
                    method="airnow",
                    dominant="o3",
                    pollutants=[
                        AirQualityPollutant(
                            type="o3",
                            name="ozone",
                            valuePPB=22.0556,
                            valueUGM3=44.1338,
                            aqi=20,
                            category="good",
                            color="00E400",
                            method="airnow",
                        ),
                    ],
                )
            ],
            profile=AirQualityProfile(
                tz="America/Chicago", sources=[AirQualitySource(name="AirNow (EPA)")], stations=["AIRNOW_271390505"]
            ),
            relativeTo=None,
        )

        assert aq == aq

    def test_eq_equivalent_airqualitys(self) -> None:
        """
        Tests that two equivalent :py:class:`AirQuality` objects are equal.
        """
        aq1 = AirQuality(
            id=None,
            loc=Location(lat=44.85469, long=-93.47079),
            place=Place(name="eden prairie", state="mn", country="us"),
            periods=[
                AirQualityObservation(
                    dt=datetime(year=2022, month=5, day=13, hour=13, minute=0, second=0),
                    aqi=20,
                    category="good",
                    color="00E400",
                    method="airnow",
                    dominant="o3",
                    pollutants=[
                        AirQualityPollutant(
                            type="o3",
                            name="ozone",
                            valuePPB=22.0556,
                            valueUGM3=44.1338,
                            aqi=20,
                            category="good",
                            color="00E400",
                            method="airnow",
                        ),
                    ],
                )
            ],
            profile=AirQualityProfile(
                tz="America/Chicago", sources=[AirQualitySource(name="AirNow (EPA)")], stations=["AIRNOW_271390505"]
            ),
            relativeTo=None,
        )
        aq2 = AirQuality(
            id=None,
            loc=Location(lat=44.85469, long=-93.47079),
            place=Place(name="eden prairie", state="mn", country="us"),
            periods=[
                AirQualityObservation(
                    dt=datetime(year=2022, month=5, day=13, hour=13, minute=0, second=0),
                    aqi=20,
                    category="good",
                    color="00E400",
                    method="airnow",
                    dominant="o3",
                    pollutants=[
                        AirQualityPollutant(
                            type="o3",
                            name="ozone",
                            valuePPB=22.0556,
                            valueUGM3=44.1338,
                            aqi=20,
                            category="good",
                            color="00E400",
                            method="airnow",
                        ),
                    ],
                )
            ],
            profile=AirQualityProfile(
                tz="America/Chicago", sources=[AirQualitySource(name="AirNow (EPA)")], stations=["AIRNOW_271390505"]
            ),
            relativeTo=None,
        )

        assert aq1 == aq2

    def test_not_eq_airquality_other_object(self) -> None:
        """
        Tests that an object of a different type is not equal to a :py:class:`AirQuality`.
        """
        aq = AirQuality(
            id=None,
            loc=Location(lat=44.85469, long=-93.47079),
            place=Place(name="eden prairie", state="mn", country="us"),
            periods=[
                AirQualityObservation(
                    dt=datetime(year=2022, month=5, day=13, hour=13, minute=0, second=0),
                    aqi=20,
                    category="good",
                    color="00E400",
                    method="airnow",
                    dominant="o3",
                    pollutants=[
                        AirQualityPollutant(
                            type="o3",
                            name="ozone",
                            valuePPB=22.0556,
                            valueUGM3=44.1338,
                            aqi=20,
                            category="good",
                            color="00E400",
                            method="airnow",
                        ),
                    ],
                )
            ],
            profile=AirQualityProfile(
                tz="America/Chicago", sources=[AirQualitySource(name="AirNow (EPA)")], stations=["AIRNOW_271390505"]
            ),
            relativeTo=None,
        )

        assert aq != object()

    def test_not_eq_nonequivalent_airqualitys(self) -> None:
        """
        Tests that two non-equivalent :py:class:`AirQuality` objects are not equal.
        """
        aq1 = AirQuality(
            id=None,
            loc=Location(lat=44.85469, long=-93.47079),
            place=Place(name="eden prairie", state="mn", country="us"),
            periods=[
                AirQualityObservation(
                    dt=datetime(year=2022, month=5, day=13, hour=13, minute=0, second=0),
                    aqi=20,
                    category="good",
                    color="00E400",
                    method="airnow",
                    dominant="o3",
                    pollutants=[
                        AirQualityPollutant(
                            type="o3",
                            name="ozone",
                            valuePPB=22.0556,
                            valueUGM3=44.1338,
                            aqi=20,
                            category="good",
                            color="00E400",
                            method="airnow",
                        ),
                    ],
                )
            ],
            profile=AirQualityProfile(
                tz="America/Chicago", sources=[AirQualitySource(name="AirNow (EPA)")], stations=["AIRNOW_271390505"]
            ),
            relativeTo=None,
        )
        aq2 = AirQuality(
            id=None,
            loc=Location(lat=44.85469, long=-93.47079),
            place=Place(name="eden prairie", state="mn", country="us"),
            periods=[
                AirQualityObservation(
                    # note: day different from aq1
                    dt=datetime(year=2022, month=5, day=14, hour=13, minute=0, second=0),
                    aqi=20,
                    category="good",
                    color="00E400",
                    method="airnow",
                    dominant="o3",
                    pollutants=[
                        AirQualityPollutant(
                            type="o3",
                            name="ozone",
                            # note: valuePPB, valueUGM3 different from aq1
                            valuePPB=22.2461,
                            valueUGM3=44.5143,
                            aqi=20,
                            category="good",
                            color="00E400",
                            method="airnow",
                        ),
                    ],
                )
            ],
            profile=AirQualityProfile(
                tz="America/Chicago", sources=[AirQualitySource(name="AirNow (EPA)")], stations=["AIRNOW_271390505"]
            ),
            relativeTo=None,
        )

        assert aq1 != aq2

    def test_airquality_repr_is_str(self) -> None:
        """
        Tests that :py:meth:`AirQuality.__repr__` returns a string.
        """
        aq = AirQuality(
            id=None,
            loc=Location(lat=44.85469, long=-93.47079),
            place=Place(name="eden prairie", state="mn", country="us"),
            periods=[
                AirQualityObservation(
                    dt=datetime(year=2022, month=5, day=13, hour=13, minute=0, second=0),
                    aqi=20,
                    category="good",
                    color="00E400",
                    method="airnow",
                    dominant="o3",
                    pollutants=[
                        AirQualityPollutant(
                            type="o3",
                            name="ozone",
                            valuePPB=22.0556,
                            valueUGM3=44.1338,
                            aqi=20,
                            category="good",
                            color="00E400",
                            method="airnow",
                        ),
                    ],
                )
            ],
            profile=AirQualityProfile(
                tz="America/Chicago", sources=[AirQualitySource(name="AirNow (EPA)")], stations=["AIRNOW_271390505"]
            ),
            relativeTo=None,
        )

        assert isinstance(aq.__repr__(), str)

"""
tests/client/test_airquality
----------------------------

Tests functionality in the aerisweather_api_v1.client.airquality module.
"""

from datetime import datetime, timedelta, timezone
from http import HTTPStatus

from geojson import Feature, Point

from testhelper import load_test_data
from testhelper.requests import MockSession, make_response, request_equals

from aerisweather_api_v1.client import AerisApiClient
from aerisweather_api_v1.model.common import (
    Location as Loc,
    Place as P,
    RelativeTo,
    RouteGeoJsonFeature,
)
from aerisweather_api_v1.model.airquality import (
    AirQuality as AQ,
    AirQualityObservation as Obs,
    AirQualityPollutant as Pollutant,
    AirQualitySource as Src,
    AirQualityProfile as Profile,
)
from aerisweather_api_v1.model.response import AerisApiResponse

TZ_MINUS_4 = timezone(timedelta(hours=-4))
TZ_MINUS_5 = timezone(timedelta(hours=-5))


class TestAerisApiAirQualityEndpoint:
    """
    Tests the functionality of the :py:class:`AerisApiAirQualityEndpoint`.
    """

    def test_id_55344(self, aeris_api_mock_client: AerisApiClient, mock_session: MockSession) -> None:
        """
        Validates the return value of the air quality endpoint for the id-55344 test case.
        """
        mock_response_body = load_test_data("client/airquality/id-55344.txt")
        mock_session.add_response(HTTPStatus.OK, mock_response_body)

        expected_periods = [
            Obs(
                dt=datetime(year=2022, month=4, day=27, hour=13, minute=0, second=0, tzinfo=TZ_MINUS_5),
                aqi=20,
                category="good",
                color="00E400",
                method="airnow",
                dominant="o3",
                pollutants=[
                    Pollutant(
                        type="o3",
                        name="ozone",
                        valuePPB=22.0556,
                        valueUGM3=44.1338,
                        aqi=20,
                        category="good",
                        color="00E400",
                        method="airnow",
                    ),
                    Pollutant(
                        type="pm2.5",
                        name="particle matter (<2.5µm)",
                        valuePPB=None,
                        valueUGM3=3.7072,
                        aqi=15,
                        category="good",
                        color="00E400",
                        method="airnow",
                    ),
                    Pollutant(
                        type="co",
                        name="carbon monoxide",
                        valuePPB=132.7919,
                        valueUGM3=152.1896,
                        aqi=1,
                        category="good",
                        color="00E400",
                        method="airnow",
                    ),
                    Pollutant(
                        type="no2",
                        name="nitrogen dioxide",
                        valuePPB=4.159,
                        valueUGM3=8.6256,
                        aqi=4,
                        category="good",
                        color="00E400",
                        method="airnow",
                    ),
                    Pollutant(
                        type="so2",
                        name="sulfur dioxide",
                        valuePPB=0,
                        valueUGM3=0,
                        aqi=0,
                        category="good",
                        color="00E400",
                        method="airnow",
                    ),
                ],
            ),
        ]
        expected_profile = Profile(
            tz="America/Chicago",
            sources=[
                Src("AirNow (EPA)"),
                Src("Minnesota Pollution Control Agency"),
                Src("US EPA AirNow"),
                Src("OpenAQ"),
                Src("CAMS"),
            ],
            stations=[
                "AIRNOW_271390505",
                "OPENAQ_US03FC368",
                "AIRNOW_270530963",
                "OPENAQ_US3E5619E",
                "AIRNOW_270530954",
                "OPENAQ_US81D1528",
                "AIRNOW_270530962",
                "OPENAQ_USC46A0E8",
                "OPENAQ_US6C6607E",
                "AIRNOW_270370480",
            ],
        )
        expected = AerisApiResponse(
            http_response=make_response(None, HTTPStatus.OK, None),
            success=True,
            error=None,
            api_response=[
                AQ(
                    id=None,
                    loc=Loc(44.85469, -93.47079),
                    place=P("eden prairie", "mn", "us"),
                    periods=expected_periods,
                    profile=expected_profile,
                    relativeTo=None,
                ),
            ],
        )

        actual = aeris_api_mock_client.airquality.id("55344")

        assert expected == actual

    def test_search_mn_limit_5(self, aeris_api_mock_client: AerisApiClient, mock_session: MockSession) -> None:
        """
        Validates the return value of the air quality endpoint for the search-mn-limit-5 test case.
        """
        mock_response_body = load_test_data("client/airquality/search-mn-limit-5.txt")
        mock_session.add_response(HTTPStatus.OK, mock_response_body)

        expected_response = [
            AQ(
                id="AIRNOW_270031001",
                loc=Loc(45.400799, -93.201103),
                place=P("bethel", "mn", "us"),
                periods=[
                    Obs(
                        dt=datetime(year=2022, month=4, day=27, hour=15, minute=0, second=0, tzinfo=TZ_MINUS_5),
                        aqi=44,
                        category="good",
                        color="00E400",
                        method="airnow",
                        dominant="o3",
                        pollutants=[
                            Pollutant(
                                type="o3",
                                name="ozone",
                                valuePPB=48,
                                valueUGM3=96,
                                aqi=44,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                        ],
                    ),
                ],
                profile=Profile(
                    tz="America/Chicago",
                    sources=[
                        Src("AirNow (EPA)"),
                        Src("Minnesota Pollution Control Agency"),
                    ],
                    stations=["AIRNOW_270031001"],
                ),
                relativeTo=None,
            ),
            AQ(
                id="AIRNOW_270031002",
                loc=Loc(45.1425, -93.2139),
                place=P("blaine", "mn", "us"),
                periods=[
                    Obs(
                        dt=datetime(year=2022, month=4, day=27, hour=15, minute=0, second=0, tzinfo=TZ_MINUS_5),
                        aqi=42,
                        category="good",
                        color="00E400",
                        method="airnow",
                        dominant="o3",
                        pollutants=[
                            Pollutant(
                                type="co",
                                name="carbon monoxide",
                                valuePPB=100,
                                valueUGM3=114.5,
                                aqi=1,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                            Pollutant(
                                type="no2",
                                name="nitrogen dioxide",
                                valuePPB=0,
                                valueUGM3=0.188,
                                aqi=0,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                            Pollutant(
                                type="o3",
                                name="ozone",
                                valuePPB=46,
                                valueUGM3=92,
                                aqi=42,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                            Pollutant(
                                type="pm10",
                                name="particle matter (<10µm)",
                                valuePPB=None,
                                valueUGM3=6,
                                aqi=5,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                            Pollutant(
                                type="pm2.5",
                                name="particle matter (<2.5µm)",
                                valuePPB=None,
                                valueUGM3=2,
                                aqi=8,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                            Pollutant(
                                type="so2",
                                name="sulfur dioxide",
                                valuePPB=0,
                                valueUGM3=0,
                                aqi=0,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                        ],
                    ),
                ],
                profile=Profile(
                    tz="America/Chicago",
                    sources=[
                        Src("AirNow (EPA)"),
                        Src("Minnesota Pollution Control Agency"),
                    ],
                    stations=["AIRNOW_270031002"],
                ),
                relativeTo=None,
            ),
            AQ(
                id="AIRNOW_270052013",
                loc=Loc(46.8511, -95.8467),
                place=P("detroit lakes", "mn", "us"),
                periods=[
                    Obs(
                        dt=datetime(year=2022, month=4, day=27, hour=15, minute=0, second=0, tzinfo=TZ_MINUS_5),
                        aqi=44,
                        category="good",
                        color="00E400",
                        method="airnow",
                        dominant="o3",
                        pollutants=[
                            Pollutant(
                                type="o3",
                                name="ozone",
                                valuePPB=48,
                                valueUGM3=96,
                                aqi=44,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                        ],
                    ),
                ],
                profile=Profile(
                    tz="America/Chicago",
                    sources=[
                        Src("AirNow (EPA)"),
                        Src("Minnesota Pollution Control Agency"),
                    ],
                    stations=["AIRNOW_270052013"],
                ),
                relativeTo=None,
            ),
            AQ(
                id="AIRNOW_270072304",
                loc=Loc(47.878159, -95.029172),
                place=P("redby", "mn", "us"),
                periods=[
                    Obs(
                        dt=datetime(year=2022, month=4, day=27, hour=15, minute=0, second=0, tzinfo=TZ_MINUS_5),
                        aqi=8,
                        category="good",
                        color="00E400",
                        method="airnow",
                        dominant="pm2.5",
                        pollutants=[
                            Pollutant(
                                type="pm2.5",
                                name="particle matter (<2.5µm)",
                                valuePPB=None,
                                valueUGM3=2,
                                aqi=8,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                        ],
                    ),
                ],
                profile=Profile(
                    tz="America/Chicago",
                    sources=[
                        Src("AirNow (EPA)"),
                        Src("Minnesota Pollution Control Agency"),
                    ],
                    stations=["AIRNOW_270072304"],
                ),
                relativeTo=None,
            ),
            AQ(
                id="AIRNOW_270177417",
                loc=Loc(46.713694, -92.511722),
                place=P("cloquet", "mn", "us"),
                periods=[
                    Obs(
                        dt=datetime(year=2022, month=4, day=27, hour=15, minute=0, second=0, tzinfo=TZ_MINUS_5),
                        aqi=37,
                        category="good",
                        color="00E400",
                        method="airnow",
                        dominant="o3",
                        pollutants=[
                            Pollutant(
                                type="o3",
                                name="ozone",
                                valuePPB=41,
                                valueUGM3=82,
                                aqi=37,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                            Pollutant(
                                type="pm2.5",
                                name="particle matter (<2.5µm)",
                                valuePPB=None,
                                valueUGM3=1,
                                aqi=4,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                        ],
                    ),
                ],
                profile=Profile(
                    tz="America/Chicago",
                    sources=[
                        Src("AirNow (EPA)"),
                        Src("Minnesota Pollution Control Agency"),
                    ],
                    stations=["AIRNOW_270177417"],
                ),
                relativeTo=None,
            ),
        ]

        expected = AerisApiResponse(
            http_response=make_response(None, HTTPStatus.OK, None),
            success=True,
            error=None,
            api_response=expected_response,
        )

        actual = aeris_api_mock_client.airquality.search(query="state:mn", limit=5)

        assert actual == expected

    def test_closest_austin_tx(self, aeris_api_mock_client: AerisApiClient, mock_session: MockSession) -> None:
        """
        Validates the return value of the air quality endpoint for the closest-austin-tx test case.
        """
        mock_response_body = load_test_data("client/airquality/closest-austin-tx.txt")
        mock_session.add_response(HTTPStatus.OK, mock_response_body)

        expected_response = [
            AQ(
                id="AIRNOW_840484531619",
                loc=Loc(30.250845, -97.721277),
                place=P("austin", "tx", "us"),
                periods=[
                    Obs(
                        dt=datetime(year=2022, month=4, day=29, hour=9, minute=0, second=0, tzinfo=TZ_MINUS_5),
                        aqi=19,
                        category="good",
                        color="00E400",
                        method="airnow",
                        dominant="o3",
                        pollutants=[
                            Pollutant(
                                type="o3",
                                name="ozone",
                                valuePPB=21,
                                valueUGM3=42,
                                aqi=19,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                        ],
                    ),
                ],
                profile=Profile(
                    tz="America/Chicago",
                    sources=[
                        Src("AirNow (EPA)"),
                        Src("Capital Area Council of Governments"),
                    ],
                    stations=["AIRNOW_840484531619"],
                ),
                relativeTo=RelativeTo(
                    lat=30.26715,
                    long=-97.74306,
                    bearing=131,
                    bearingENG="SE",
                    distanceKM=2.768,
                    distanceMI=1.72,
                ),
            ),
            AQ(
                id="OPENAQ_US3AC0B92",
                loc=Loc(30.250845, -97.721277),
                place=P("city of austin electric utility", "tx", "us"),
                periods=[
                    Obs(
                        dt=datetime(year=2022, month=4, day=29, hour=9, minute=0, second=0, tzinfo=TZ_MINUS_5),
                        aqi=0,
                        category="good",
                        color="00E400",
                        method="airnow",
                        dominant="o3",
                        pollutants=[
                            Pollutant(
                                type="o3",
                                name="ozone",
                                valuePPB=0,
                                valueUGM3=0.021,
                                aqi=0,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                        ],
                    ),
                ],
                profile=Profile(
                    tz="America/Chicago",
                    sources=[
                        Src("US EPA AirNow"),
                        Src("Capital Area Council of Governments"),
                        Src("OpenAQ"),
                    ],
                    stations=["OPENAQ_US3AC0B92"],
                ),
                relativeTo=RelativeTo(
                    lat=30.26715,
                    long=-97.74306,
                    bearing=131,
                    bearingENG="SE",
                    distanceKM=2.768,
                    distanceMI=1.72,
                ),
            ),
        ]
        expected = AerisApiResponse(
            http_response=make_response(None, HTTPStatus.OK, None),
            success=True,
            error=None,
            api_response=expected_response,
        )

        actual = aeris_api_mock_client.airquality.closest(p="austin,tx", limit=2)

        assert expected == actual

    def test_within_nyc_limit_2(self, aeris_api_mock_client: AerisApiClient, mock_session: MockSession) -> None:
        """
        Validates the return value of the air quality endpoint for the within-nyc-limit-2 test case.
        """
        mock_response_body = load_test_data("client/airquality/within-nyc-limit-2.txt")
        mock_session.add_response(HTTPStatus.OK, mock_response_body)

        expected_response = [
            AQ(
                id="AIRNOW_360810120",
                loc=Loc(40.7269, -73.8933),
                place=P("middle village", "ny", "us"),
                periods=[
                    Obs(
                        dt=datetime(year=2022, month=4, day=29, hour=15, minute=0, second=0, tzinfo=TZ_MINUS_4),
                        aqi=6,
                        category="good",
                        color="00E400",
                        method="airnow",
                        dominant="pm2.5",
                        pollutants=[
                            Pollutant(
                                type="pm2.5",
                                name="particle matter (<2.5µm)",
                                valuePPB=None,
                                valueUGM3=1.5,
                                aqi=6,
                                category="good",
                                color="00E400",
                                method="airnow",
                            )
                        ],
                    ),
                ],
                profile=Profile(
                    tz="America/New_York",
                    sources=[
                        Src("AirNow (EPA)"),
                        Src("New York Dept. of Environmental Conservation"),
                    ],
                    stations=["AIRNOW_360810120"],
                ),
                relativeTo=None,
            ),
            AQ(
                id="OPENAQ_US64790F0",
                loc=Loc(40.7269, -73.8933),
                place=P("columbusville (historical)", "ny", "us"),
                periods=[
                    Obs(
                        dt=datetime(year=2022, month=4, day=29, hour=15, minute=0, second=0, tzinfo=TZ_MINUS_4),
                        aqi=6,
                        category="good",
                        color="00E400",
                        method="airnow",
                        dominant="pm2.5",
                        pollutants=[
                            Pollutant(
                                type="pm2.5",
                                name="particle matter (<2.5µm)",
                                valuePPB=None,
                                valueUGM3=1.5,
                                aqi=6,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                        ],
                    ),
                ],
                profile=Profile(
                    tz="America/New_York",
                    sources=[
                        Src("US EPA AirNow"),
                        Src("New York Dept. of Environmental Conservation"),
                        Src("OpenAQ"),
                    ],
                    stations=["OPENAQ_US64790F0"],
                ),
                relativeTo=None,
            ),
        ]

        expected = AerisApiResponse(
            http_response=make_response(None, HTTPStatus.OK, None),
            success=True,
            error=None,
            api_response=expected_response,
        )

        actual = aeris_api_mock_client.airquality.within(p="40.79775,-73.9735,40.63807,-73.745549", limit=2)

        assert expected == actual

    def test_route_mpls_mn_to_rochester_mn(
        self, aeris_api_mock_client: AerisApiClient, mock_url: str, mock_session: MockSession
    ) -> None:
        """
        Validates the return value of the air quality endpoint for the route-mpls-mn-to-rochester-mn test case.
        """
        mock_response_body = load_test_data("client/airquality/route-mpls-mn-to-rochester-mn.txt")
        mock_session.add_response(HTTPStatus.OK, mock_response_body)

        expected_response = [
            AQ(
                id=None,
                loc=Loc(44.9739, -93.2668),
                place=P("minneapolis", "mn", "us"),
                periods=[
                    Obs(
                        dt=datetime(year=2022, month=5, day=1, hour=10, minute=0, second=0, tzinfo=TZ_MINUS_5),
                        aqi=13,
                        category="good",
                        color="00E400",
                        method="airnow",
                        dominant="o3",
                        pollutants=[
                            Pollutant(
                                type="o3",
                                name="ozone",
                                valuePPB=14.5,
                                valueUGM3=29.0145,
                                aqi=13,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                            Pollutant(
                                type="pm2.5",
                                name="particle matter (<2.5µm)",
                                valuePPB=None,
                                valueUGM3=1,
                                aqi=4,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                            Pollutant(
                                type="pm10",
                                name="particle matter (<10µm)",
                                valuePPB=None,
                                valueUGM3=1,
                                aqi=1,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                            Pollutant(
                                type="co",
                                name="carbon monoxide",
                                valuePPB=181.0087,
                                valueUGM3=207.436,
                                aqi=2,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                            Pollutant(
                                type="no2",
                                name="nitrogen dioxide",
                                valuePPB=2,
                                valueUGM3=4.0465,
                                aqi=2,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                            Pollutant(
                                type="so2",
                                name="sulfur dioxide",
                                valuePPB=0,
                                valueUGM3=0,
                                aqi=0,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                        ],
                    ),
                ],
                profile=Profile(
                    tz="America/Chicago",
                    sources=[
                        Src("AirNow (EPA)"),
                        Src("Minnesota Pollution Control Agency"),
                        Src("US EPA AirNow"),
                        Src("OpenAQ"),
                        Src("CAMS"),
                    ],
                    stations=[
                        "AIRNOW_270530954",
                        "OPENAQ_US81D1528",
                        "AIRNOW_270530962",
                        "OPENAQ_USC46A0E8",
                        "OPENAQ_US3E5619E",
                        "AIRNOW_270530963",
                        "OPENAQ_US946D297",
                        "AIRNOW_270530910",
                        "OPENAQ_USE3A8D47",
                        "AIRNOW_270530909",
                    ],
                ),
                relativeTo=None,
            ).with_geojson(
                Feature(
                    id="44.9739,-93.2668",
                    geometry=Point((-93.2668, 44.9739)),
                    properties={
                        "request": {
                            "error": None,
                            "id": "44.9739,-93.2668",
                            "skipped": False,
                            "success": True,
                        }
                    },
                )
            ),
            AQ(
                id=None,
                loc=Loc(44.023, -92.4629),
                place=P("rochester", "mn", "us"),
                periods=[
                    Obs(
                        dt=datetime(year=2022, month=5, day=1, hour=11, minute=0, second=0, tzinfo=TZ_MINUS_5),
                        aqi=14,
                        category="good",
                        color="00E400",
                        method="airnow",
                        dominant="o3",
                        pollutants=[
                            Pollutant(
                                type="o3",
                                name="ozone",
                                valuePPB=15,
                                valueUGM3=30,
                                aqi=14,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                            Pollutant(
                                type="pm2.5",
                                name="particle matter (<2.5µm)",
                                valuePPB=None,
                                valueUGM3=1.1,
                                aqi=5,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                            Pollutant(
                                type="pm10",
                                name="particle matter (<10µm)",
                                valuePPB=None,
                                valueUGM3=1.5,
                                aqi=1,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                            Pollutant(
                                type="co",
                                name="carbon monoxide",
                                valuePPB=140,
                                valueUGM3=160,
                                aqi=2,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                            Pollutant(
                                type="no2",
                                name="nitrogen dioxide",
                                valuePPB=2,
                                valueUGM3=3.76,
                                aqi=2,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                            Pollutant(
                                type="so2",
                                name="sulfur dioxide",
                                valuePPB=0,
                                valueUGM3=0.262,
                                aqi=0,
                                category="good",
                                color="00E400",
                                method="airnow",
                            ),
                        ],
                    )
                ],
                profile=Profile(
                    tz="America/Chicago",
                    sources=[Src("CAMS")],
                    stations=[],
                ),
                relativeTo=None,
            ).with_geojson(
                Feature(
                    id="1",
                    geometry=Point((-92.4629, 44.023)),
                    properties={
                        "request": {
                            "id": "1",
                            "skipped": False,
                            "success": True,
                            "error": None,
                        }
                    },
                )
            ),
        ]

        expected = AerisApiResponse(
            http_response=make_response(None, HTTPStatus.OK, None),
            success=True,
            error=None,
            api_response=expected_response,
        )

        route = [
            RouteGeoJsonFeature(Point((-93.2668, 44.9739)), id="0"),
            RouteGeoJsonFeature(Point((-92.4629, 44.0230)), id="1", from_="+90minutes"),
        ]
        actual = aeris_api_mock_client.airquality.route(route=route)
        sent_request = mock_session.send_mock.call_args[0][0]

        assert expected == actual
        assert request_equals(
            request=sent_request,
            path="airquality/route",
            query=aeris_api_mock_client.http.params,
            body=[r.as_dict() for r in route],
        )

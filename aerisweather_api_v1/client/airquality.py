"""
aerisweather_api_v1/client/airquality
-------------------------------------

Contains code for the Aeris API v1 client airquality endpoint.
"""

from typing import Optional

from ..model.common import Route
from ..model.response import AerisApiResponse
from ..model.airquality import AirQuality
from .endpoint import AerisApiEndpoint


class AerisApiAirQualityEndpoint(AerisApiEndpoint[AirQuality]):
    """
    Air Quality endpoint for the Aeris API v1.
    """

    path = "airquality"
    docs = "https://www.aerisweather.com/support/docs/api/reference/endpoints/airquality/"

    def id(
        self,
        id: str,
        filter: Optional[str] = None,
        query: Optional[str] = None,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        sort: Optional[str] = None,
        plimit: Optional[int] = None,
        pskip: Optional[int] = None,
        radius: Optional[str] = None,
        mindist: Optional[str] = None,
    ) -> AerisApiResponse[AirQuality]:
        """
        Performs a request against the air quality endpoint's :aerisapi_epact:`:id <airquality>` action.

        :param id: location or station ID to query information for
        :param filter: filter to limit results returned; see the :aerisapi_epfilt:`supported filters <airquality>`
        :param query: query based on given properties; \
            see the :aerisapi_epquery:`supported query properties <airquality>`
        :param limit: limit total number of results returned
        """
        query_params = self._prepare_params(locals())
        return self._request("GET", id, query_params)

    __call__ = id

    def closest(
        self,
        p: Optional[str] = None,
        filter: Optional[str] = None,
        query: Optional[str] = None,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        sort: Optional[str] = None,
        plimit: Optional[int] = None,
        pskip: Optional[int] = None,
        radius: Optional[str] = None,
        mindist: Optional[str] = None,
    ) -> AerisApiResponse[AirQuality]:
        query_params = self._prepare_params(locals())
        return self._request("GET", "closest", query_params)

    def search(
        self,
        p: Optional[str] = None,
        filter: Optional[str] = None,
        query: Optional[str] = None,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        sort: Optional[str] = None,
        plimit: Optional[int] = None,
        pskip: Optional[int] = None,
        radius: Optional[str] = None,
        mindist: Optional[str] = None,
    ) -> AerisApiResponse[AirQuality]:
        query_params = self._prepare_params(locals())
        return self._request("GET", "search", query_params)

    def within(
        self,
        p: Optional[str] = None,
        filter: Optional[str] = None,
        query: Optional[str] = None,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        sort: Optional[str] = None,
        plimit: Optional[int] = None,
        pskip: Optional[int] = None,
        radius: Optional[str] = None,
        mindist: Optional[str] = None,
    ) -> AerisApiResponse[AirQuality]:
        query_params = self._prepare_params(locals())
        return self._request("GET", "within", query_params)

    def route(
        self,
        route: Route,
        filter: Optional[str] = None,
        query: Optional[str] = None,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        sort: Optional[str] = None,
        plimit: Optional[int] = None,
        pskip: Optional[int] = None,
        radius: Optional[str] = None,
        mindist: Optional[str] = None,
    ) -> AerisApiResponse[AirQuality]:
        query_params = self._prepare_params(locals())
        data = [r.as_dict() for r in route]
        return self._request("POST", "route", query_params, data)

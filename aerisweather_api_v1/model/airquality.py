"""
aerisweather/api/v1/model/airquality
------------------------------------

Contains model definitions for the Aeris API v1 airquality endpoint.
"""

from datetime import datetime
from typing import Any, List, Optional

from ..util import optisclose
from .common import ApiModel, Location, Place, Profile, RelativeTo


class AirQualityPollutant:
    """
    Class representing an air quality pollutant returned by the Aeris API v1.

    For information about the fields of this model, consult the
    :aerisapi_epprop:`Aeris API air quality documentation <airquality>`.

    :param type: a short identifier of the pollutant, e.g. "o3", "pm2.5", or "co"
    :param name: the name of the pollutant, e.g. "ozone", "particle matter (<2.5µm)", or "carbon monoxide"
    :param valuePPB: the pollutant's concentration in the air in parts per billion
    :param valueUGM3: the pollutant's concentration in the air in micrograms per cubic meter
    :param aqi: the pollutant concentration as an air quality index (0 <= aqi <= 500)
    :param category: the air quality category based on `aqi`, e.g. "good", "moderate", "unhealthy", "hazardous"
    :param color: the hexadecimal color code associated with `category`, e.g. "00E400"
    :param method: the method used to calculate `aqi`
    """

    def __init__(
        self,
        type: str,
        name: str,
        valuePPB: Optional[float],
        valueUGM3: Optional[float],
        aqi: int,
        category: str,
        color: str,
        method: str,
    ) -> None:
        self.type = type
        self.name = name
        self.valuePPB = valuePPB
        self.valueUGM3 = valueUGM3
        self.aqi = aqi
        self.category = category
        self.color = color
        self.method = method

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if ``other`` is a :py:class:`AirQualityPollutant` with the same
        attributes as this one, otherwise returns False.

        :param other: another object
        """
        if not isinstance(other, self.__class__):
            return False

        return (
            self.type == other.type
            and self.name == other.name
            and optisclose(self.valuePPB, other.valuePPB)
            and optisclose(self.valueUGM3, other.valueUGM3)
            and self.aqi == other.aqi
            and self.category == other.category
            and self.color == other.color
            and self.method == other.method
        )

    def __repr__(self) -> str:
        if self.valuePPB is not None:
            return f"{self.__class__.__name__}({self.name}, PPB={self.valuePPB})"
        else:
            return f"{self.__class__.__name__}({self.name}, UGM^3={self.valueUGM3})"


class AirQualityObservation:
    """
    Class representing a single air quality observation returned by the Aeris API v1.

    For information about the fields of this model, consult the
    :aerisapi_epprop:`Aeris API air quality documentation <airquality>`.

    :param dt: the datetime for this air quality observation
    :param aqi: the air quality index value (0 <= aqi <= 500)
    :param category: the air quality category based on `aqi`, e.g. "good", "moderate", "unhealthy", "hazardous"
    :param color: the hexadecimal color code associated with `category`, e.g. "00E400"
    :param method: the method used to calculate `aqi`
    :param dominant: the type of the dominant pollutant, e.g. "co", "o3", "pm10"
    :param pollutants: a list of pollutants present in the air
    """

    def __init__(
        self,
        dt: datetime,
        aqi: int,
        category: str,
        color: str,
        method: str,
        dominant: str,
        pollutants: List[AirQualityPollutant],
    ) -> None:
        self.datetime = dt
        self.aqi = aqi
        self.category = category
        self.color = color
        self.method = method
        self.dominant = dominant
        self.pollutants = pollutants

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if ``other`` is a :py:class:`AirQualityObservation` with the same
        attributes as this one, otherwise returns False.

        :param other: another object
        """
        if not isinstance(other, self.__class__):
            return False

        return (
            self.datetime == other.datetime
            and self.aqi == other.aqi
            and self.category == other.category
            and self.color == other.color
            and self.method == other.method
            and self.dominant == other.dominant
            and self.pollutants == other.pollutants
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(datetime={self.datetime}, aqi={self.aqi}, pollutants={self.pollutants})"


class AirQualitySource:
    """
    Class representing an air quality source returned by the Aeris API v1.

    For information about the fields of this model, consult the
    :aerisapi_epprop:`Aeris API air quality documentation <airquality>`.

    :param name: the name of the source
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if ``other`` is a :py:class:`AirQualitySource` with the same
        attributes as this one, otherwise returns False.

        :param other: another object
        """
        if not isinstance(other, self.__class__):
            return False

        return self.name == other.name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"


class AirQualityProfile(Profile):
    """
    Class representing an air quality profile returned by the Aeris API v1.

    For information about the fields of this model, consult the
    :aerisapi_epprop:`Aeris API air quality documentation <airquality>`.

    :param tz: the timezone associated with the :py:class:`location <LocationV1>`
    :param sources: list of sources that provided the air quality information
    :param stations: list of station IDs that provided the air quality information
    """

    def __init__(self, tz: str, sources: List[AirQualitySource], stations: List[str]) -> None:
        super().__init__(tz)
        self.sources = sources
        self.stations = stations

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if ``other`` is a :py:class:`AirQualityProfile` with the same
        attributes as this one, otherwise returns False.

        :param other: another object
        """
        if not isinstance(other, self.__class__):
            return False

        return self.tz == other.tz and self.sources == other.sources and self.stations == other.stations

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(sources={self.sources}, stations={self.stations})"


class AirQuality(ApiModel):
    """
    Class representing an air quality result returned by the Aeris API v1.

    For information about this model, consult the
    :aerisapi_epprop:`Aeris API air quality documentation <airquality>`.

    :param id: the ID of the station returning the data, if data is from a single station
    :param loc: the location of the air quality record
    :param place: the place of the air quality record
    :param periods: a list of air quality observations
    :param relativeTo: observation location relative to requested location
    """

    def __init__(
        self,
        id: Optional[str],
        loc: Location,
        place: Place,
        periods: List[AirQualityObservation],
        profile: AirQualityProfile,
        relativeTo: Optional[RelativeTo],
    ) -> None:
        super().__init__()

        self.id = id
        self.loc = loc
        self.place = place
        self.periods = periods
        self.profile = profile
        self.relativeTo = relativeTo

    def __eq__(self, other: Any) -> bool:
        """
        Returns True if ``other`` is a :py:class:`AirQuality` with the same
        attributes as this one, otherwise returns False.

        :param other: another object
        """
        if not isinstance(other, self.__class__):
            return False

        return (
            self.id == other.id
            and self.loc == other.loc
            and self.place == other.place
            and self.profile == other.profile
            and self.periods == other.periods
            and self.relativeTo == other.relativeTo
            and self.geojson == other.geojson
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.loc}, {self.place}, {self.profile}, {self.periods})"

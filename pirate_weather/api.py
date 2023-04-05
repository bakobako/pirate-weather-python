from datetime import datetime
from enum import Enum
import aiohttp

from .forecast import Forecast
from .request_manager import BaseRequestManger, RequestManger, RequestMangerAsync
from .types import languages, units, weather


class PirateWeatherApiVersion(str, Enum):
    BASE = "https://api.pirateweather.net/forecast"
    TIME_MACHINE = "https://timemachine.pirateweather.net/forecast"


class BasePirateWeather:

    def __init__(self, api_key: str):
        self.api_key: str = api_key
        self.request_manager: BaseRequestManger = None

    def get_forecast(
            self,
            latitude: float,
            longitude: float,
            extend: bool = None,
            lang=languages.ENGLISH,
            values_units=units.AUTO,
            exclude: [weather] = None,
            timezone: str = None,
    ):
        raise NotImplementedError

    def get_time_machine_forecast(
            self,
            latitude: float,
            longitude: float,
            time: datetime,
            extend: bool = False,
            lang=languages.ENGLISH,
            values_units=units.AUTO,
            exclude: [weather] = None,
            timezone: str = None,
    ):
        raise NotImplementedError

    def get_url(self, latitude: float, longitude: float, time=None, api_version=PirateWeatherApiVersion.BASE, **params):
        host = api_version
        valid_lat_long = self.validate_lat_long(latitude=latitude, longitude=longitude)
        if not valid_lat_long:
            raise ValueError("Invalid Latitude or Longitude values.")
        if time is None:
            return "{host}/{api_key}/{latitude},{longitude}".format(
                api_key=self.api_key,
                host=host,
                latitude=latitude,
                longitude=longitude,
            )
        return "{host}/{api_key}/{latitude},{longitude},{time}".format(
            api_key=self.api_key,
            host=host,
            latitude=latitude,
            longitude=longitude,
            time=time,
        )

    @staticmethod
    def validate_lat_long(latitude: float, longitude: float):
        """
        Validate latitude and longitude values.

        Parameters:
        latitude (float): Latitude value in degrees.
        longitude (float): Longitude value in degrees.

        Returns:
        bool: True if the latitude and longitude values are valid, False otherwise.
        """
        if -90.0 <= latitude <= 90.0:
            if -180.0 <= longitude <= 180.0:
                return True
        return False


class PirateWeather(BasePirateWeather):
    def __init__(self, api_key: str, gzip: bool = True):
        super().__init__(api_key)
        self.request_manager = RequestManger(gzip)

    def get_forecast(
            self,
            latitude: float,
            longitude: float,
            extend: bool = None,
            lang=languages.ENGLISH,
            values_units=units.AUTO,
            exclude: [weather] = None,
            timezone: str = None,
    ) -> Forecast:
        url = self.get_url(latitude, longitude)
        data = self.request_manager.make_request(
            url=url,
            extend=weather.HOURLY if extend else None,
            lang=lang,
            units=values_units,
            exclude=exclude,
            timezone=timezone,
        )
        return Forecast(**data)

    def get_time_machine_forecast(
            self,
            latitude: float,
            longitude: float,
            time: datetime,
            extend: bool = False,
            lang=languages.ENGLISH,
            values_units=units.AUTO,
            exclude: [weather] = None,
            timezone: str = None,
    ) -> Forecast:
        url = self.get_url(latitude, longitude, int(time.timestamp()), api_version=PirateWeatherApiVersion.TIME_MACHINE)
        data = self.request_manager.make_request(
            url=url,
            extend=weather.HOURLY if extend else None,
            lang=lang,
            units=values_units,
            exclude=exclude,
            timezone=timezone,
        )
        return Forecast(**data)


class PirateWeatherAsync(BasePirateWeather):
    def __init__(
            self,
            api_key: str,
            gzip: bool = True
    ):
        super().__init__(api_key)
        self.request_manager = RequestMangerAsync(
            gzip=gzip
        )

    async def get_forecast(self,
                           latitude: float,
                           longitude: float,
                           client_session: aiohttp.ClientSession,
                           extend: bool = None,
                           lang=languages.ENGLISH,
                           values_units=units.AUTO,
                           exclude: [weather] = None,
                           timezone: str = None,
                           ) -> Forecast:
        url = self.get_url(latitude, longitude)
        data = await self.request_manager.make_request(
            url=url,
            extend=weather.HOURLY if extend else None,
            lang=lang,
            units=values_units,
            exclude=exclude,
            timezone=timezone,
            session=client_session,
        )
        return Forecast(**data)

    async def get_time_machine_forecast(self,
                                        latitude: float,
                                        longitude: float,
                                        time: datetime,
                                        client_session: aiohttp.ClientSession,
                                        extend: bool = False,
                                        lang=languages.ENGLISH,
                                        values_units=units.AUTO,
                                        exclude: [weather] = None,
                                        timezone: str = None
                                        ) -> Forecast:
        url = self.get_url(latitude, longitude, int(time.timestamp()))
        data = await self.request_manager.make_request(
            url=url,
            extend=weather.HOURLY if extend else None,
            lang=lang,
            units=values_units,
            exclude=exclude,
            timezone=timezone,
            session=client_session,
        )
        return Forecast(**data)

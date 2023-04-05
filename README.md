Pirate Weather Python
==========

This library for the [Pirate Weather API](https://pirateweather.net) which is an alternative to the deprecated DarkSky
API, and provides access to detailed
weather information from around the globe.

* [Installation](#installation)
* [Get started](#get-started)
* [Contact us](#contact-us)
* [License](#license)

## This library was made by updating the [darksky library by Detrous](https://github.com/Detrous/darksky) so all credits go to them.

### Installation

```
pip3 install pirate_weather_python
```

### Get started

Before you start using this library, you need to get your API key
[here](https://pirate-weather.apiable.io/).

All classes are fully annotated, source code is your best doc : )

Use of synchronous client:

```python
from pirate_weather.api import PirateWeather
from pirate_weather.types import languages, units, weather

API_KEY = "0123456789"
pirate_weather = PirateWeather(API_KEY)

latitude = 42.3601
longitude = -71.0589
forecast = pirate_weather.get_forecast(
    latitude, longitude,
    extend=False,  # default `False`
    lang=languages.ENGLISH,  # default `ENGLISH`
    values_units=units.AUTO,  # default `auto`
    exclude=[weather.MINUTELY, weather.ALERTS],  # default `[]`,
    timezone='UTC'  # default None - will be set by DarkSky API automatically
)
```

Use of synchronous timemachine client:

```python
from pirate_weather.api import PirateWeather
from pirate_weather.types import languages, units, weather
from datetime import datetime as dt

API_KEY = "0123456789"
pirate_weather = PirateWeather(API_KEY)
t = dt(2022, 5, 6, 12)

latitude = 42.3601
longitude = -71.0589
forecast = pirate_weather.get_time_machine_forecast(
    latitude, longitude,
    extend=False,  # default `False`
    lang=languages.ENGLISH,  # default `ENGLISH`
    values_units=units.AUTO,  # default `auto`
    exclude=[weather.MINUTELY, weather.ALERTS],  # default `[]`,
    timezone='UTC',  # default None - will be set by DarkSky API automatically
    time=t
)
```

Use of asynchronous client:

```python
from pirate_weather.api import PirateWeatherAsync
from pirate_weather.types import languages, units, weather

import asyncio
import aiohttp


async def main(api_key):
    async with aiohttp.ClientSession() as session:
        darksky = PirateWeatherAsync(api_key)

        latitude = 42.3601
        longitude = -71.0589
        forecast = await darksky.get_forecast(
            latitude, longitude,
            extend=False,  # default `False`
            lang=languages.ENGLISH,  # default `ENGLISH`
            values_units=units.AUTO,  # default `auto`
            exclude=[weather.MINUTELY, weather.ALERTS],  # default `[]`
            timezone='UTC',  # default None - will be set by DarkSky API automatically,
            client_session=session  # default aiohttp.ClientSession()
        )

api_key = "0123456789"
asyncio.run(main(api_key))
```

### License.

Library is released under the [MIT License](./LICENSE).
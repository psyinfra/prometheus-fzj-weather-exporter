#!/usr/bin/env python3
# This file is licensed under the ISC license.
# Oskar Druska 2022
# For further information look up LICENSE.txt

from dataclasses import dataclass
from prometheus_fzj_weather_exporter import fzj_weather


@dataclass
class Weather:
    temperature: float  # celsius
    air_pressure: float  # hectoPascal
    humidity: int  # percent
    wind_power: float  # beaufort
    wind_direction: int  # degree

def fzj_weather_crawler(insec_bool):
    """ scrapes data from the FZJ weather site via the fzj_weather.py script
        and returns a dataclass object containing the information """

    crawled_weather_data = fzj_weather.get_weather_data(insec_bool)
    
    weather_return = Weather(
        temperature=float(crawled_weather_data['Lufttemperatur']),
        air_pressure=float(crawled_weather_data['Luftdruck (92 m ü.N.H.N.)']),
        humidity=int(crawled_weather_data['relative Feuchte']),
        wind_power=float(crawled_weather_data['Windstärke']),
        wind_direction=int(crawled_weather_data['Windrichtung'])
    )

    return weather_return
#!/usr/bin/env python3
# This file is licensed under the ISC license.
# Oskar Druska 2022
# For further information look up LICENSE.txt

from prometheus_client import Summary
from prometheus_client.core import GaugeMetricFamily

from . import fzj_weather_crawler

REQUEST_TIME = Summary("weather_exporter_collect_seconds",
                       "Time spent to collect metrics from fzj_weather.py")


class FZJWeatherExporter:
    insec : bool

    def __init__(self, insec_bool) -> None:
        self.insec = insec_bool

    @REQUEST_TIME.time()
    def collect(self):

        weather = fzj_weather_crawler.fzj_weather_crawler(self.insec)

        g = GaugeMetricFamily(
            name='fzj_weather_air_temperature_celsius',
            documentation='temperature in celcius')
        g.add_metric([], weather.temperature)
        yield g

        g = GaugeMetricFamily(
            name='fzj_weather_air_pressure_hectopascal',
            documentation='air pressure in hectopascal')
        g.add_metric([], weather.air_pressure)
        yield g

        g = GaugeMetricFamily(
            name='fzj_weather_humidity_percent',
            documentation='humidity in percent')
        g.add_metric([], weather.humidity)
        yield g

        g = GaugeMetricFamily(
            name='fzj_weather_wind_power_beaufort',
            documentation='wind power in beaufort')
        g.add_metric([], weather.wind_power)
        yield g

        g = GaugeMetricFamily(
            name='fzj_weather_wind_direction_degree',
            documentation='wind direction in degree')
        g.add_metric([], weather.wind_direction)
        yield g

# FZJ-Weather Prometheus Exporter
The FZJ-Weather Prometheus Exporter (short: exporter) provides weather data in
the format specified for Prometheus Exporters. It consists of two parts:
  1. `fzj_weather.py`: a python script using BeautifulSoup4 and requests to
     parse and return meteorological data from a weather station inside the
     Forschungszentrum Jülich (short: FZJ). It does so by parsing the website
     providing the information.
  2. exporter (`main.py`): uses said script to receive, parse and provide
     the data to the Prometheus database. Once started, it runs indefinitely
     until interrupted.

`main.py` references the weather script and other needed scripts. It therefore
marks the entry point of the exporter.

## Installation and Usage
1. Install the package from the corresponding GitHub Repository:
    `pip install git+https://github.com/psyinfra/prometheus_fzj_weather_exporter.git`
2. Start the exporter:
    `prometheus_fzj_weather_exporter`
3. (from another terminal) `curl 127.0.0.1:9184`

Or

1. Clone the project:
    `git clone git@github.com:psyinfra/prometheus-fzj-weather-exporter.git`
2. Install dependencies from inside the repository:
    `pip install -e .`
3. Start the exporter:
    `python prometheus_fzj_weather_exporter/main.py --web.listen-address 127.0.0.1:9184`
4. (from another terminal) `curl 127.0.0.1:9184`

The output of `curl 127.0.0.1:9184` has this structure (similar for the other data
i.e. air pressure, humidity, wind power, wind direction):

```
# HELP fzj_weather_air_temperature temperature in celsius
# TYPE fzj_weather_air_temperature gauge
fzj_weather_air_temperature 14.0
```

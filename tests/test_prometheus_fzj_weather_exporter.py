import pytest

from prometheus_fzj_weather_exporter.fzj_weather_crawler import fzj_weather_crawler

# variables to crawl weather data
LISTEN_ADDRESS = "127.0.0.1:9184"
WEATHER_URL = "https://www.fz-juelich.de/de/gs/ueber-uns/meteo/aktuelle-wetterdaten/wetterdaten"


@pytest.mark.vcr()
def test_scrape_weather_website() -> None:
    """Crawl the fzj weather website and verify that data of the expected
    data type was received."""

    # get weather data
    weather_data = fzj_weather_crawler(WEATHER_URL,
                                       insecure=False)

    # verify contents
    assert isinstance(weather_data.temperature, float)
    assert isinstance(weather_data.air_pressure, float)
    assert isinstance(weather_data.humidity, int)
    assert isinstance(weather_data.wind_power, float)
    assert isinstance(weather_data.wind_direction, int)

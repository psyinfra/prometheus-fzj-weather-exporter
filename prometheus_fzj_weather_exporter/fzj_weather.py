#!/usr/bin/env python3
# This file is licensed under the ISC license.
# Oskar Druska 2022
# For further information look up LICENSE

# This script parses weather data from an FZJ inside website

import requests
import re
from bs4 import BeautifulSoup


def get_weather_data(url: str,
                     insecure: bool) -> dict:
    # if `insecure`, then Request shall ignore the SSL certificate
    r = requests.get(url, verify=(not insecure))
    if r.status_code != 200:
        raise ConnectionError(f"Something's wrong with the Website:\n{url}\n{r.status_code}")

    soup = BeautifulSoup(r.text, 'html.parser')
    weather_dict = make_weather_dict(url, soup)

    return weather_dict


def make_weather_dict(url, soup) -> dict:
    """Parses the table containing weather information from the webpage into a
    dictionary with headers as keys and data as values (i.e. Luftdruck: 1016.6 hPa).
    """
    weather_table = soup.table.find_all("tr")
    weather_data = {
        "source": url,
        "title": soup.title.get_text(strip=True),
        "date": soup.u.get_text(strip=True)
    }

    for row in weather_table:
        weather_td = row.find_all("td")  # td: table data

        # `replace(u'\xa0', u' ')` replaces parsing errors with whitespaces
        # `re.sub('[^0-9 , .]', ''` strips all non-numeric characters from the string
        weather_data[weather_td[0].get_text(strip=True).replace(u'\xa0', u' ')] \
            = re.sub('[^0-9 , .]', '', weather_td[1].get_text(strip=True))

    return weather_data

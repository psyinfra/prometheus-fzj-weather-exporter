#!/usr/bin/env python3
# This file is licensed under the ISC license.
# Oskar Druska 2022
# For further information look up LICENSE.txt

# This script parses weather data from an FZJ inside website

import requests
import re
from bs4 import BeautifulSoup


# Python module to execute

def get_weather_data(insec_bool):
    url = "https://www.fz-juelich.de/de/gs/ueber-uns/meteo/aktuelle-wetterdaten/wetterdaten"

    r = requests.get(url, verify = not insec_bool) # if insec_bool, then Request shall ignore the SSL certificate

    if r.status_code != 200:
        raise ConnectionError("Something's wrong with the Website:\n" + url + "\n" + str(r.status_code))

    soup = BeautifulSoup(r.text, 'html.parser')

    weather_dict = make_weather_dict(url, soup)  # {header: data}

    return weather_dict


def make_weather_dict(url, soup):
    # Parses the table containing the needed information to get all table rows.
    weather_tablerows = soup.table.find_all("tr")

    # Creates a dictionary with headers as keys and data as values
    # (i.e. Luftdruck: 1016.6 hPa).
    # `.replace(u'\xa0', u' ')` replaces parsing errors with whitespaces
    # `re.sub('[^0-9 , .]', '', weather_td[1].get_text(strip=True)` strips
    # all non-numeric characters from the string

    weather_data = {
        "source": url,
        "title": soup.title.get_text(strip=True),
        "date": soup.u.get_text(strip=True)
    }

    for row in weather_tablerows:
        weather_td = row.find_all("td")  # td, table data

        weather_data[weather_td[0].get_text(strip=True).replace(u'\xa0', u' ')] \
            = re.sub('[^0-9 , .]', '', weather_td[1].get_text(strip=True))

    return weather_data

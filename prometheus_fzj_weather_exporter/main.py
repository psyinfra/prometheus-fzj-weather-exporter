#!/usr/bin/env python3
# This file is licensed under the ISC license.
# Oskar Druska 2022
# For further information look up LICENSE

import sys
import argparse
from argparse import RawTextHelpFormatter
import time
from prometheus_client import start_http_server, REGISTRY
from prometheus_fzj_weather_exporter import exporter_file


def main():
    args = get_parsed_args()
    url = "https://www.fz-juelich.de/de/gs/ueber-uns/meteo/aktuelle-wetterdaten/wetterdaten"
    try:
        REGISTRY.register(exporter_file.FZJWeatherExporter(url, args.insecure))
    except ConnectionError as c:
        sys.exit(c.strerror)

    # start the http server
    if args.listenaddress:
        ip, port = args.listenaddress.split(":")
        if ip:
            start_http_server(port=int(port), addr=ip)
        else:  # listen on all interfaces
            start_http_server(port=int(port))
    else:
        start_http_server(port=9184, addr='127.0.0.1')

    # keep the exporter running indefinitely
    while True:
        time.sleep(1)


def get_parsed_args():
    parser = argparse.ArgumentParser(
        description='Set up the Prometheus exporter (connection ports)',
        formatter_class=RawTextHelpFormatter)
    group = parser.add_argument_group()
    group.add_argument(
        '-w', '--web.listen-address',
        type=str,
        dest='listenaddress',
        help='Address and port to expose metrics and web interface. Default: ":9184"\n'
             'To listen on all interfaces, omit the IP: ":<port>"\n'
             'To listen on a specific IP: <address>:<port>')
    group.add_argument(
        '-i', '--insecure',
        dest='insecure',
        action='store_true',
        default=False,
        help='Skip SSL validation of the weather website.')

    return parser.parse_args()


if __name__ == '__main__':
    main()

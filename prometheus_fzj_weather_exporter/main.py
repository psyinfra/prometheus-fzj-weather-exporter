#!/usr/bin/env python3
# This file is licensed under the ISC license.
# Oskar Druska 2022
# For further information look up LICENSE.txt

# exporter entry point

# usage:    > python3 main.py --web.listen-address 9184
# test:     > curl 127.0.0.1:9184
# (test in a different console or start in background)
# expected output (similar to):
# > # HELP fzj_weather_air_temperature temperature in celsius
# > # TYPE fzj_weather_air_temperature gauge
# > fzj_weather_air_temperature 14.0
# (equivalent output for other data i.e. humidity)

import sys
import argparse
import time
from prometheus_client import start_http_server, REGISTRY
from . import exporter_file


def main():
    args = get_parsed_args()

    try:
        REGISTRY.register(exporter_file.FZJWeatherExporter(args.insecure))
    except ConnectionError as c:
        sys.exit(c.strerror)

    if args.listenaddress is None:
        start_http_server(port=9184, addr='127.0.0.1')
    else:
        ip, port = args.listenaddress.split(":")
        if ip:
            start_http_server(port=int(port), addr=ip)
        else:  # listen on all interfaces
            start_http_server(port=int(port))

    # keep the thing going indefinitely
    while True:
        time.sleep(1)


def get_parsed_args():
    parser = argparse.ArgumentParser(
        description='Set up the Prometheus exporter (connection ports)')
    group = parser.add_argument_group()
    group.add_argument(
        '-w', '--web.listen-address',
        type=str,
        dest='listenaddress',
        help='Address and port to expose metrics and web interface. Default: ":9184"\n'
                'To listen on all interfaces, omit the IP. ":<port>"`\n'\
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

#!/usr/bin/env python3
# This file is licensed under the ISC license.
# Oskar Druska 2022
# For further information look up LICENSE.txt

# exporter entry point

# usage:    > python3 main.py --port 9840
# test:     > curl 127.0.0.1:9840
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

    if args.port is None:
        start_http_server(port=9840, addr='127.0.0.1')
    else:
        ip = args.port.split(":")
        if len(ip) == 1: #when only a port was specified; no ":"in args.port => split has length == 1"
            start_http_server(port=int(ip[0]))
        else:
            start_http_server(port=int(ip[1]), addr=str(ip[0]))
    
    # keep the thing going indefinitely
    while True:
        time.sleep(1)


def get_parsed_args():
    parser = argparse.ArgumentParser(
        description='Set up the Prometheus exporter (connection ports)')
    mutual_group = parser.add_mutually_exclusive_group()
    mutual_group.add_argument(
        '-p', '--port',
        type=str,
        dest='port',
        help='IP address of the machine to run the script on.\n'\
                'If you only wanna specify the port, do so via `--port <port>`\n'\
                'If you wanna use a whole IP addres: `--port <address>:<port>`')
    mutual_group.add_argument(
        '-i', '--insecure',
        dest='insecure',
        action='store_true',
        default=False,
        help='If True, ignores the SSL certificate of the website, pulling the information from.')

    return parser.parse_args()


if __name__ == '__main__':
    main()

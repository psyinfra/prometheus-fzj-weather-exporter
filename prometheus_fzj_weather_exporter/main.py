#!/usr/bin/env python3
# This file is licensed under the ISC license.
# Oskar Druska 2022
# For further information look up LICENSE.txt

# exporter entry point

# usage:    > python3 main.py --port :9840
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

    REGISTRY.register(exporter_file.FZJWeatherExporter())

    if not len(sys.argv) > 1:
        start_http_server(port=9840, addr='127.0.0.1') # Default, if no args were given
    elif args.port is not None:
        start_http_server(args.port)
    elif args.ip is not None:
        port = int(args.ip.split(":")[1])
        addr = str(args.ip.split(":")[0])
        start_http_server(port=port, addr=addr) # --port and --insecure are mutually exclusive and None as per default

    # keep the thing going indefinitely
    while True:
        time.sleep(1)


def get_parsed_args():
    parser = argparse.ArgumentParser(
        description='Set up the Prometheus exporter (connection ports)')
    mutual_group = parser.add_mutually_exclusive_group()
    mutual_group.add_argument(
        '-p', '--port',
        type=int,
        dest='port',
        help='Port of this machine to run the script on')
    mutual_group.add_argument(
        '-i', '--insecure',
        type=str,
        dest='ip',
        help='Full IP address of the server to run the script on; including port')

    return parser.parse_args()


if __name__ == '__main__':
    main()

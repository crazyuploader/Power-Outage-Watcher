#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the main file for the project.
"""

__author__ = "Jugal Kishore <me@devjugal.com>"

import time
from config_parser import load_config, get_apprise_urls
from parsers.cesc_mysore import parse_mysore_power_outage
from utilies import get_natural_time

# Load the configuration file
config = load_config("config.yaml")
apprise_urls = get_apprise_urls(config)


def main():
    """
    Main function to execute the script.
    """
    print("Starting PowerOutageWatch script...")

    while True:
        # Parse the Mysore Power Outage page
        outages = parse_mysore_power_outage(
            config["settings"]["outage_page_urls"]["cesc_mysore"]
        )

        # Print the parsed outage information
        print(outages)

        # Wait for the specified interval before checking again
        duration = config["settings"]["check_interval"]
        print("Sleeping for {}...".format(get_natural_time(duration)))
        time.sleep(duration)


if __name__ == "__main__":
    main()

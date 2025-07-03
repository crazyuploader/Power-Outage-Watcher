#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the main file for the project.
"""

__author__ = "Jugal Kishore <me@devjugal.com>"


from parsers.cesc_mysore import parse_mysore_power_outage

# Global Variable(s)
MYSORE_POWER_OUTAGE_URL = "https://cescmysore.karnataka.gov.in/new-page/Scheduled Power Interruption information 2025-26/en"


def main():
    """
    Main function to execute the script.
    """
    print("Starting PowerOutageWatch script...")

    # Parse the Mysore Power Outage page
    outages = parse_mysore_power_outage(MYSORE_POWER_OUTAGE_URL)

    # Print the parsed outage information
    print(outages)


if __name__ == "__main__":
    main()

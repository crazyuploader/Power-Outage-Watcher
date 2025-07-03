"""
utilities.py

This module provides utility functions for the Power Outage Watcher application.
"""

__author__ = "Jugal Kishore <me@devjugal.com>"

import datetime as dt
import humanize


def get_natural_time(seconds):
    """
    Convert seconds to a human-readable format.

    Args:
        seconds (int): The number of seconds to convert.

    Returns:
        str: A human-readable string representing the time duration.
    """
    delta = dt.timedelta(seconds=seconds)
    return humanize.precisedelta(delta)

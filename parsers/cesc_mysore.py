#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cesc_mysore.py

This module is responsible for parsing the HTML content of the Mysore Power Outage
information page. It extracts scheduled outage dates and their associated PDF links.
"""

__author__ = "Jugal Kishore <me@devjugal.com>"

# pylint: disable=R0914

from typing import List, Dict, Any
from bs4 import BeautifulSoup
import requests
import urllib3

# Suppress only InsecureRequestWarning
# This is used because the target website might be using
# an outdated TLS configuration, which can trigger warnings.
urllib3.disable_warnings()


def parse_mysore_power_outage(url: str) -> List[Dict[str, Any]]:
    """
    Parse the HTML content of the Mysore Power Outage page and extract outage information.

    Args:
        url (str): The URL of the Mysore Power Outage page.

    Returns:
        list: A list of dictionaries, where each dictionary contains
            'date' and 'pdf_links' for each outage entry.
    """
    try:
        # Send a GET request to the URL.
        # allow_redirects=True: Follows any redirects.
        # timeout=60: Sets a timeout of 60 seconds for the request.
        # verify=False: Disables SSL certificate verification. Use with caution.
        response = requests.get(url, allow_redirects=True, timeout=60, verify=False)
        # Raise an HTTPError for bad responses (4xx or 5xx client/server errors).
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Re-raise the exception to be handled by the calling function (e.g., main.py)
        # This allows for centralized error logging and notification for critical failures.
        print(f"CRITICAL ERROR: Failed to fetch {url}. Error: {e}")
        raise  # Re-raise the exception after printing a local message.

    # Parse the HTML content of the response using BeautifulSoup.
    soup = BeautifulSoup(response.text, "html.parser")
    outages: List[Dict[str, Any]] = []

    # Locate the main container div that holds the outage table.
    # This provides a more specific target for finding the table.
    table_container = soup.find("div", id="table-archive")
    if not table_container:
        print(
            "ERROR: Could not find the table container with id 'table-archive'. "
            "HTML structure might have changed."
        )
        return outages

    # Locate the specific table containing the outage data within its container.
    table = table_container.find("table", class_="table-striped")
    if not table:
        print(
            "ERROR: Could not find the table with class 'table-striped' inside "
            "the 'table-archive' container. HTML structure might have changed."
        )
        return outages

    # Find all table rows (<tr>) within the identified table.
    rows = table.find_all("tr")

    # Iterate over the rows, skipping the first row as it typically contains table headers.
    for row in rows[1:]:
        # Find all table data cells (<td>) within the current row.
        cols = row.find_all("td")

        # Ensure there are at least two columns: one for date and one for PDF link(s).
        if len(cols) >= 2:
            # Extract the text content of the first column (Date).
            # .get_text(strip=True) removes leading/trailing whitespace.
            date: str = cols[0].get_text(strip=True)
            pdf_links: List[str] = []
            link_cell = cols[1]  # The second column contains the PDF link(s).

            # Find all <a> (anchor) tags within the second column that have an 'href' attribute.
            # This handles cases where multiple PDF links might be present for a single date.
            anchors = link_cell.find_all("a", href=True)
            for anchor in anchors:
                pdf_link = anchor["href"]
                # Basic check to ensure the href value ends with '.pdf', indicating a PDF file.
                if pdf_link.endswith(".pdf"):
                    pdf_links.append(pdf_link)

            # Only add the entry if actual PDF links were found for this date.
            if pdf_links:
                outage_info: Dict[str, Any] = {
                    "date": date,
                    "pdf_links": pdf_links,
                }
                outages.append(outage_info)
            else:
                # Log a warning if a date entry exists but no valid PDF links were found.
                print(
                    f"WARNING: No PDF links found for date: {date} in the expected format."
                )
        else:
            # Log a warning if a row doesn't have the expected number of columns.
            print(
                f"WARNING: Skipping row due to unexpected column count: {row.prettify()}"
            )

    return outages

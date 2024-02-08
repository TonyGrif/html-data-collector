#!/usr/bin/env python3

"""Main module for the html data collector."""

import argparse
import logging

import requests


def main():
    """Main driver of the html data collector script."""
    parser = argparse.ArgumentParser(
        description="Gather text from an HTTP response and store for later analysis."
    )

    parser.add_argument("uri", type=str, help="The URI to gather text from.")

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        dest="logging_level",
        const=logging.INFO,
        help="Output verbose info logs to console.",
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_const",
        dest="logging_level",
        const=logging.DEBUG,
        help="Output all program debug logs to console.",
    )

    args = parser.parse_args()
    # TODO: Set specific loggers, not all at once
    logging.basicConfig(level=args.logging_level)

    logging.info("Requesting:%s", args.uri)

    try:
        request = requests.get(args.uri, timeout=5)
    except (
        requests.exceptions.MissingSchema,
        requests.exceptions.InvalidURL,
        requests.exceptions.ConnectionError,
    ):
        logging.error("Request failed on %s", args.uri)
        return
    except requests.Timeout:
        logging.error("%s time reached, aborting request on %s", 5, args.uri)
        return

    logging.info("Response returned")


if __name__ == "__main__":
    main()

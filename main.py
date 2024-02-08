#!/usr/bin/env python3

"""Main module for the html data collector."""

import argparse
import logging


def main():
    """Main driver of the html data collector script."""
    parser = argparse.ArgumentParser(
        description="Gather text from an HTTP response and store for later analysis."
    )

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


if __name__ == "__main__":
    main()

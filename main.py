#!/usr/bin/env python3

"""Main module for the html data collector."""

import argparse
import csv
import hashlib
import logging
from pathlib import Path

import requests
from boilerpy3 import extractors


def main():
    """Main driver of the html data collector script."""
    parser = argparse.ArgumentParser(
        description="Gather text from an HTTP response and store for later analysis."
    )

    parser.add_argument("uri", type=str, help="The URI to gather text from.")

    parser.add_argument(
        "-T",
        metavar="timeout",
        dest="timeout",
        nargs="?",
        type=float,
        default=5,
        help="The time before a HTTP request times out.",
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

    logging.info("Requesting:%s", args.uri)

    try:
        response = requests.get(args.uri, timeout=args.timeout)
    except (
        requests.exceptions.MissingSchema,
        requests.exceptions.InvalidURL,
        requests.exceptions.ConnectionError,
    ):
        logging.error("Request failed on %s", args.uri)
        return
    except requests.Timeout:
        logging.error("%s time reached, aborting request on %s", args.timeout, args.uri)
        return

    logging.info("Response returned")

    extractor = extractors.ArticleExtractor(raise_on_failure=False)
    content = extractor.get_content(response.text)

    if len(content) == 0:
        logging.error("Not enough information gathered, aborting")
        return

    hash_val = hashlib.md5(args.uri.encode("utf-8").strip())
    logging.info("Hash generated: %s", hash_val.hexdigest())

    org_path = Path(f"output/original/{hash_val.hexdigest()}.txt")
    org_path.parent.mkdir(exist_ok=True, parents=True)
    boil_path = Path(f"output/processed/{hash_val.hexdigest()}.txt")
    boil_path.parent.mkdir(exist_ok=True, parents=True)

    with open("output/KEYS.csv", "a+", encoding="utf-8") as keys:
        keys.seek(0)
        exists = f"{args.uri}\n" in keys.readlines()
        if not exists:
            logging.info("Adding URI to KEYS.txt")
            writer = csv.writer(keys, delimiter=",")
            writer.writerow([f"{hash_val.hexdigest()}", f"{args.uri}"])
        else:
            logging.info("URI is already present in KEYS.txt")

    with open(org_path, "w", encoding="utf-8") as org, open(
        boil_path, "w", encoding="utf-8"
    ) as bog:
        logging.info("Writing text to %s", org_path)
        org.write(response.text)

        logging.info("Writing text to %s", boil_path)
        bog.write(content)


if __name__ == "__main__":
    main()

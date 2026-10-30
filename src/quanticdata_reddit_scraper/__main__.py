"""`python -m quanticdata_reddit_scraper` and the `reddit-scraper` command."""

import os
import sys

from ._qd.cli import load_spec, main


def run() -> None:
    sys.exit(main(load_spec(os.path.dirname(os.path.abspath(__file__)))))


if __name__ == "__main__":
    run()

import argparse
import logging

from oogg.browser import open_with_browser
from oogg.repository import repository

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
logger = logging.getLogger("main")


def create_parser() -> argparse.Namespace:
    """Create the argument parser for the application.

    :return: The namespace with the parsed args
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--owner",
        help="Username associated with the repository.",
        default=repository.owner,
    )
    parser.add_argument(
        "--repository",
        help="Name of the repository.",
        default=repository.repo,
    )
    parser.add_argument(
        "--host",
        help="The host of the provider.",
        default=repository.host,
    )
    parser.add_argument(
        "--branch",
        help="Branch of the repository.",
        default=repository.branch,
    )
    parser.add_argument(
        "filepath",
        help="The desired path of the file (Can include the line number with a"
        "#<number> or #<from-number>-<to-number>)",
    )

    return parser.parse_args()


def main() -> int:
    """Main entrypoint for the oogg application.

    :return: int as a return code
    :rtype: int
    """
    args = create_parser()

    return open_with_browser(args)

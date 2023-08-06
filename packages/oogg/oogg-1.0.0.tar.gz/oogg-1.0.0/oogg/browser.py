import argparse
import logging
import subprocess
import sys
from typing import Dict
from urllib.parse import unquote
from urllib.parse import urlparse

from oogg.repository import repository

_PROVIDERS: Dict[str, str] = {
    "github": "https://{host}/{owner}/{repo}/blob/{branch}/{file}",
    "gitlab": "https://{host}/{owner}/{repo}/-/blob/{branch}/{file}",
    "bitbucket": "https://{host}/{owner}/{repo}/src/{branch}/{file}",
}  # : Hashmap of providers to their url patterns

logger = logging.getLogger("browser")


def open_with_browser(args: argparse.Namespace) -> int:
    """Open the given pathfile in the browser

    This method will used the favorite browser of the user by actually calling
    them using `xdg-open` on unix, `open` on MacOS and `start` on win32.

    :param args: The arguments passed from the CLI.
    :type args: int
    :return: The return code of the subprocess call
    :rtype: int
    """
    try:
        provider = _PROVIDERS[repository.platform]
    except KeyError:
        logger.error(
            f"Couldn't find any template for provider {repository.platform}.",
        )
        return 1

    parsed_filepath = urlparse(unquote(args.filepath))

    url = provider.format(
        host=args.host,
        owner=args.owner,
        repo=args.repository,
        branch=args.branch,
        file=parsed_filepath.path,
    )

    if parsed_filepath.fragment:
        line_number = f"#L{parsed_filepath.fragment}"

        if "-" in parsed_filepath.fragment:
            start, end = tuple(parsed_filepath.fragment.split("-"))
            line_number = f"#L{start}-L{end}"

        url += line_number

    cmd = "xdg-open"
    if sys.platform == "win32":
        cmd = "start"
    elif sys.platform == "darwin":
        cmd = "open"

    out = subprocess.run(
        (cmd, url),
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )

    logger.info(f"Succesfully opened your file in {repository.platform}")

    return out.returncode

import argparse
import logging
import sys

from gasbullet import skeleton as gasbullet_skeleton

from politicalsoup import __version__, filter

__author__ = "Taylor Monacelli"
__copyright__ = "Taylor Monacelli"
__license__ = "MPL-2.0"

_logger = logging.getLogger(__name__)


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Client for gasbullet.  Purpose is to test adding my filters."
    )
    parser.add_argument(
        "--version",
        action="version",
        version="politicalsoup {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    parser.add_argument(
        "-r",
        "--roots",
        dest="roots",
        help="list of root directories to scan",
        default=".",
        nargs="*",
    )
    parser.add_argument(
        "-f",
        "--list-types",
        action="store_true",
        help="report types of files",
        default=False,
    )
    parser.add_argument(
        "--no-cache", action="store_true", help="regenerate pickle file", default=False
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logformat = "{%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    gasbullet_skeleton.client(args, filter.myfilter)
    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()

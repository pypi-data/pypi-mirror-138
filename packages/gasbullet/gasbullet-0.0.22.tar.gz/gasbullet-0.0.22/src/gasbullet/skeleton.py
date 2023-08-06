import argparse
import logging
import pathlib
import sys
from typing import Dict, Set

import magic

from gasbullet import __version__
from gasbullet import cache as cachemod
from gasbullet import filter

__author__ = "Taylor Monacelli"
__copyright__ = "Taylor Monacelli"
__license__ = "MPL-2.0"

_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Just a Fibonacci demonstration")
    parser.add_argument(
        "--version",
        action="version",
        version="gasbullet {ver}".format(ver=__version__),
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


def dowork(cache: cachemod.Cache, filter_func):
    paths = set()
    for root in cache.roots:
        paths |= {str(path) for path in pathlib.Path(root).rglob("*")}

    cache.load()
    filter_func(paths, cache)


def set_mymap_magic_types(paths: Set[str], cache: cachemod.Cache) -> Dict[str, str]:
    for _str in paths:
        result = cache.mymap.get(_str, None)
        if not result:
            logging.debug(f"running magic for file path {_str}")
            cache.mymap[_str] = magic.from_file(_str, mime=True)


def client(args, filter_fcn=None):
    """Args:
    args (List[str]): command line parameters as list of strings
        (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug(f"Starting {__loader__.name}...")
    cache = cachemod.Cache(args.roots)
    if args.no_cache:
        cache.delete()
    dowork(cache, filter_fcn)

    if args.list_types:
        cache.report_types(cache.data)
    else:
        cache.show_results(cache.data)
    _logger.info("Script ends here")


def main(args):
    """Args:
    args (List[str]): command line parameters as list of strings
        (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug(f"Starting {__loader__.name}...")
    cache = cachemod.Cache(args.roots)
    if args.no_cache:
        cache.delete()
    dowork(cache, filter.myfilter)

    if args.list_types:
        cache.report_types(cache.data)
    else:
        cache.show_results(cache.data)
    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()

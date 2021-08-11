#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Microservice app wrapper with uvicorn.
"""

from os import path as os_path
from sys import exit as sys_exit, stderr as sys_stderr, version_info as sys_version_info
from errno import ENOTRECOVERABLE
from typing import Dict
from logging import basicConfig, getLogger, DEBUG, INFO
from argparse import ArgumentParser, RawTextHelpFormatter
from uvicorn import run as uvicorn_run
from app.kapibara.__constants__ import __app_name__
from app.kapibara.__constants__ import __description__
from app.kapibara.__constants__ import __version__
from app.kapibara.api import asgi as kapi_asgi


if sys_version_info < (3, 6, 0):
    sys_stderr.write(
        "Python 3.6.x or newer is needed to run this script\n")
    sys_exit(ENOTRECOVERABLE)

app = kapi_asgi()

_log = getLogger()


def parse_args() -> Dict:
    """Parse command line arguments & provide help screen for CLI.

    :return: Dictionary containing the parsed arguments
    :rtype: Dict
    """
    parser = ArgumentParser(prog=os_path.basename(__file__),
                            description=__description__,
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument("-b", "--bind", type=str, default="", metavar="addr[:port]",
                        help="bind <addr>[:<port>] to use for the microservice")
    parser.add_argument("--debug", action="store_true",
                        help="Turns ON debug mode (implies '-vv')")
    parser.add_argument("--development", action="store_true",
                        help="Turns ON development mode (reloads the server if a change is detected)")
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="Increase output verbosity")
    parser.add_argument("--version", action="version",
                        help="Show program version",
                        version=f"%(prog)s ({__app_name__} v{__version__})")
    parser.set_defaults(debug=False)
    received_args = vars(parser.parse_args())
    return received_args


def main():
    """CLI main entrypoint
    """
    args = parse_args()
    _verbose = args.get("verbose")
    fmt = "[%(levelname)-8s] %(message)s"
    if _verbose == 1:
        _log.setLevel(INFO)
        basicConfig(level=INFO, format=fmt)
    if _verbose >= 2 or args.get("debug"):
        args["debug"] = True
        args["verbose"] = 2 if _verbose < 2 else _verbose
        _log.setLevel(DEBUG)
        basicConfig(level=DEBUG, format=fmt)
    _bind = args.get("bind")
    if not _bind:
        args["bind"] = f"{app.kapi.server_addr}:{app.kapi.server_port}"
    _log.debug("Received arguments are: %s", args)

    uvicorn_run("server:app",
                host=args.get("bind", app.kapi.server_addr).split(":", 1)[0],
                port=int(args.get("bind", app.kapi.server_port).split(":", 1)[-1]),
                headers=[("server", __app_name__)],
                log_level="debug" if args.get("debug", False) else "info",
                reload=bool(args.get("development", False)),
                )


if __name__ == "__main__":
    main()

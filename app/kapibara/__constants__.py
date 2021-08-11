#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Package-wide constant definitions.

"""

from os import path as os_path
from configparser import ConfigParser
from errno import EINVAL
from re import search
from sys import exit as sys_exit
from typing import NamedTuple
from .shared.useful import find_config_path


__all__ = (
    "__version__",
    "__version_info__",
    "__author__",
    "__email__",
    "__app_name__",
    "__description__",
)


config = ConfigParser()
pkg_setup_cfg = os_path.join(
    find_config_path("setup.cfg",
                     os_path.basename(os_path.dirname(__file__))),
    "setup.cfg")
config.read(pkg_setup_cfg)

for s in ["metadata"]:
    if s not in config.sections():
        print(
            f"[ERROR] The '{pkg_setup_cfg}' configuration file does not contain a '{s}' section.")
        sys_exit(EINVAL)


__version__ = config["metadata"].get("version", "0.0.0alpha0")
_v = search(
    r"^([0-9]+)\.([0-9]+)(\.([0-9]+))*(([a-zA-z]+)([0-9]*))*$", __version__)
VersionInfo = NamedTuple("VersionInfo", [("major", int), ("minor", int),
                                         ("micro", int), ("releaselevel", str),
                                         ("serial", int)])
__version_info__ = VersionInfo(int(_v.group(1)) if _v.group(1) else 0,
                               int(_v.group(2)) if _v.group(2) else 0,
                               int(_v.group(4)) if _v.group(4) else 0,
                               str(_v.group(6)),
                               int(_v.group(7)) if _v.group(7) else 0)
__author__ = config["metadata"].get("author", "Unknown")
__email__ = config["metadata"].get("author_email", "")
__app_name__ = config["metadata"].get("name", "")
__description__ = config["metadata"].get("description", "")

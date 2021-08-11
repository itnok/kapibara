#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Install requirements sourced from setup.cfg.

This Python package concentrate all configurations inside either ``setup.cfg``
or ``setup.py`` to avoid to have multiple files to maintain with the same contents.
Usually requirements are listed in a file names ``requirements.txt`` present in the
root of the repository and used for development purposes. The same requirements are
also supposed to be listed in ``setup.cfg`` for ``setup.py`` to be able to create
a Wheel correctly and install them when ``pip`` is requested to install the Wheel.
This script supersedes and substitute the command
``python3 -m pip install -r requirements.txt``.

Example:
    To install all the needed requirements for development purposes::

        $ ./install_requirements.py

"""

from sys import exit as sys_exit, executable
from errno import EINVAL
from typing import Dict, List
from pathlib import Path, PurePath
from configparser import ConfigParser
from subprocess import check_call


class SetupCfgParser(ConfigParser):  # pylint: disable=too-many-ancestors
    """Custom configuration parser for `setup.cfg` based on built-in ConfigParser.

    """

    def get_list(self, section, option) -> List:
        """Returns all lines of a multiline `setup.cfg` option as a list.

        :param section: configuration file section to get data from
        :type section: str
        :param option:  multiline string to be retrieved as list
        :type option: str

        :return: all lines part of the source `setup.cfg` option
        :rtype: List
        """
        value = self.get(section, option)
        return list(filter(None, (x.strip() for x in value.splitlines())))

    def get_listint(self, section, option):
        """Returns all integers listed as multiline `setup.cfg` option as a list.

        :param section: configuration file section to get data from
        :type section: str
        :param option:  multiline string to be retrieved as list of integers
        :type option: str

        :return: all integers specified on multiple lines in the source `setup.cfg` option
        :rtype: List
        """
        return [int(x) for x in self.get_list(section, option)]

    def get_dict(self, section, option) -> Dict:
        """Returns all key = value pairs in a multiline `setup.cfg` option as a dictionary.

        :param section: configuration file section to get data from
        :type section: str
        :param option:  multiline string to be retrieved as dictionary
        :type option: str

        :return: all key = value pairs specified on multiple lines in the source `setup.cfg` option
        :rtype: Dict
        """
        return dict(x.split("=") for x in self.get_list(section, option))


current_path = Path(__file__).parent.absolute()

config = SetupCfgParser()
config.read(str(PurePath(current_path, "setup.cfg")))

for s in ["options"]:
    if s not in config.sections():
        print(f"[ERROR] The 'setup.cfg' configuration file does not contain a {s} section.")
        sys_exit(EINVAL)


if __name__ == "__main__":
    print("==> Installing requirements sourced from 'setup.cfg'")
    packages = config.get_list("options", "install_requires")
    check_call([executable, "-m", "pip", "install", *packages])

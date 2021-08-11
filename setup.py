#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Setup package for distribution.

This script configures the Python package for distribution re-using and leveraging
the information and metadata present in the `setup.cfg` file. This approach makes
the maintenance easier and makes sure the relevant information for distribution is
in one place only.

Example:
    To prepare the package for distribution, from CLI use the commands below.
    The first command makes sure the latest versions of PyPi’s `build` is installed.
    The second one actually does build the package. All commands must be run from the
    root directory of the project where the `pyproject.toml` file is located.
    The final artifacts will be stored in the `dist` directory::

        $ python3 -m pip install --upgrade build
        $ python3 -m build

"""

from os import path as os_path
from sys import exit as sys_exit
from errno import EINVAL
from typing import Dict, List
from pathlib import Path, PurePath
from configparser import ConfigParser
from setuptools import setup, find_packages


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

with open(str(PurePath(current_path, "README.md")), "r", encoding="utf-8") as f:
    long_description = f.read()

config = SetupCfgParser()
config.read(str(PurePath(current_path, "setup.cfg")))

for s in ["metadata", "options"]:
    if s not in config.sections():
        print(f"[ERROR] The 'setup.cfg' configuration file does not contain a {s} section.")
        sys_exit(EINVAL)

_app_name_ = config["metadata"].get("name", "")

setup(name=_app_name_,
      version=config["metadata"].get("version", "0.0.0alpha0"),
      author=config["metadata"].get("author", "nobody"),
      author_email=config["metadata"].get("author_email", ""),
      description=config["metadata"].get("description", ""),
      long_description=long_description,
      long_description_content_type="text/markdown",
      url=config["metadata"].get("url", ""),
      project_urls=config.get_dict("metadata", "project_urls"),
      classifiers=config.get_list("metadata", "classifiers"),
      package_dir={"": "app"},
      packages=find_packages(where="app"),
      data_files=[
          (os_path.join("share", _app_name_, ".config"), ["setup.cfg"]),
          (os_path.join("share", _app_name_, "examples"), [f"{_app_name_}.yml"])],
      include_package_data=True,
      license_files=["LICENSE", ],
      zip_safe=bool(config["options"].get("zip_safe", False)),
      python_requires=config["options"].get("python_requires", ">=3.6"),
      install_requires=config.get_list("options", "install_requires"),
      )

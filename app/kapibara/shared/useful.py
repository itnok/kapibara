#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Package-wide useful shared functions.

"""

from os import getcwd as os_getcwd
from os import path as os_path
from sys import prefix as sys_prefix
from logging import getLogger as l_getLogger

__all__ = (
    "find_config_path",
)


class DummyLogger():    # pylint: disable=too-few-public-methods
    """Class to create a dummy logger using at runtime.

    It should uses ``print`` under the hood to replace
    the logging facility where it is not present.

    Example to detect missing ``.debug`` of a ``logger``
    .. code-block:: python
        try:
            logger_name
        except NameError:
            logger_name = DummyLogger()
    """
    __slots__ = {
        "_logger",
    }

    def __init__(self):
        self._logger = l_getLogger()

    def debug(self, msg: str, *args):
        """Dummy no-op debug function
        """
        self._logger.debug(msg, *args)


def fstr_template(template: str) -> str:
    """Returns a string created using the provided template as if it was an f-string literal

    Example:
    .. code-block:: python
        tmplt = "A reusable template to show the value of {some_var}"
        some_var = "some-content-that-will-be-printed"
        print(fstr_template(tmplt))

    :param template: A string containing the template to use to format an f-string
    :type template: str

    :return: The interpolated formatted string
    :rtype: str
    """
    # pylint: disable=eval-used
    return str(eval(f"f'{template}'"))


def find_config_path(fname: str, appname: str = os_path.basename(os_path.splitext(__file__)[0])) -> str:
    """Returns the path to the provided file that is the most relevant for configuring purposes.

    It checks the listed paths in the following order:

    - <Directory where ``__file__`` is saved>
    - <Directory where ``__file__`` is saved>/.config
    - <Current working directory>
    - ``${HOME}`` directory
    - ``${HOME}/.config/<_APP_NAME_>``
    - ``${HOME}/.config``
    - ``${HOME}/.local/<_APP_NAME_>``
    - ``${HOME}/.local``
    - ``/etc/<_APP_NAME_>``
    - ``/etc``
    - ``<prefix>/share/<_APP_NAME_>``
    - ``<prefix>/share/<_APP_NAME_>/.config/<_APP_NAME_>``
    - ``<prefix>/share/<_APP_NAME_>/.config/``

    When in none of these locations the provided ``fname`` exists, it returns and empty string.

    :param fname: (base)name of the configuration file to look for
    :type fname: str

    :param appname: name of the application the configuration refers to
                    (defaults to the basename of the script which loaded the module)
    :type appname: str

    :return: The path to the most relevant configuration file with the provided name.
        The reseach follows the priority list described above...
    :rtype: str
    """
    try:
        log
    except NameError:
        log = DummyLogger()
    user_home = os_path.expanduser("~")
    pkg_dir = os_path.dirname(__file__)
    possible_path = [
        (os_path.realpath, pkg_dir),
        (os_path.join, (pkg_dir, ".config")),
        (os_getcwd, None),
        (os_path.realpath, user_home),
        (os_path.join, (user_home, ".config", appname)),
        (os_path.join, (user_home, ".config")),
        (os_path.join, (user_home, ".local", appname)),
        (os_path.join, (user_home, ".local")),
        (os_path.join, ("/etc", appname)),
        (os_path.realpath, "/etc"),
        (os_path.join, (sys_prefix, "share", appname)),
        (os_path.join, (sys_prefix, "share", appname, ".config", appname)),
        (os_path.join, (sys_prefix, "share", appname, ".config")),
    ]
    for fnc, params in possible_path:
        log.debug("trying %s[%s]", fnc, params)
        if isinstance(params, type(None)):
            # pylint is wrong here, because it has no clue we will always call
            # functions that accept no args here!
            cfg_path = fnc()  # pylint: disable=E1120
            # pylint: disable=E1120
        if isinstance(params, str):
            cfg_path = fnc(params)
        if isinstance(params, tuple):
            cfg_path = fnc(*params)
        if os_path.exists(os_path.join(cfg_path, fname)):
            log.debug("searching for %s, %s was found...", fname, cfg_path)
            return cfg_path
    return ""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TEST shared/useful.py

"""

from os import getcwd as os_getcwd
from os import path as os_path
from app.kapibara.shared import useful


def test_find_config_path():
    """[TEST] find_config_path
    """
    res = useful.find_config_path("setup.cfg")
    assert res == os_getcwd()
    res = useful.find_config_path("kapibara.yml")
    assert res == os_getcwd()
    res = useful.find_config_path("passwd", "")
    assert res == "/etc/"
    res = useful.find_config_path("this-file-is-unlikely-to-exist-and-will-not-be-found.txt")
    assert res == ""

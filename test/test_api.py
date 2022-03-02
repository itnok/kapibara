#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TEST api.py

"""

from sys import maxsize as sys_maxsize
from random import seed as rnd_seed
from random import randint as rnd_randint
from fastapi import status
from fastapi.testclient import TestClient

from app.kapibara.api import app
from app.kapibara.api import Kapibara
from app.kapibara.__constants__ import __app_name__

client = TestClient(app)

def test_class_kapibara_singleton():
    """[TEST] Class Kapibara is correctly behaving as a SINGLETON
    """
    rnd_seed()
    k = Kapibara()
    for i in range(10):
        random_port_num = rnd_randint(1000, 65535)
        k.conf["server"]["port"] = random_port_num
        new_k = Kapibara()
        assert k._instance == new_k._instance
        assert id(k) == id(new_k)
        assert k.conf["server"]["port"] == random_port_num
        assert new_k.conf["server"]["port"] == random_port_num

def test_get_root():
    """[TEST] get_root
    """
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"Hello": "World", "from": __app_name__}


def test_get_items():
    """[TEST] get_items
    """
    params = (
        {},
        {"q": None},
        {"q": "string"},
        {"q": "string containing spaces"},
        {"q": "insanely long string " * 4096},
        {"q": "utf-8 $trìng ∞ \U00002764 wïth \U0001F9A5"},
        {"q": ""},
        {"q": "None"},
        {"q": "undefined"},
        {"q": "123456"},
    )
    rnd_seed()
    for i in range(10):
        random_id = rnd_randint(-sys_maxsize, sys_maxsize)
        response = client.get(f"/items/{random_id}", params=params[i])
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == (
            {"item_id": random_id, "q": params[i]["q"]}
            if params[i] else
            {"item_id": random_id, "q": None})


def test_get_items_validation():
    """[TEST] get_items (422 - Validation error)
    """
    response = client.get("/items/string")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_plaintext():
    """[TEST] get_plaintext
    """
    response = client.get("/plaintext")
    assert response.status_code == status.HTTP_200_OK
    assert response.text == "nothing more than text..."

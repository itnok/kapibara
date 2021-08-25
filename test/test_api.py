#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TEST api.py

"""

from sys import maxsize as sys_maxsize
from random import seed as rnd_seed
from random import randint as rnd_randint
from fastapi.testclient import TestClient

from app.kapibara.api import app
from app.kapibara.__constants__ import __app_name__

client = TestClient(app)


def test_get_root():
    """[TEST] get_root
    """
    response = client.get("/")
    assert response.status_code == 200
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
        assert response.status_code == 200
        assert response.json() == (
            {"item_id": random_id, "q": params[i]["q"]}
            if params[i] else
            {"item_id": random_id, "q": None})


def test_get_items_validation():
    """[TEST] get_items (422 - Validation error)
    """
    response = client.get("/items/string")
    assert response.status_code == 422


def test_get_plaintext():
    """[TEST] get_plaintext
    """
    response = client.get("/plaintext")
    assert response.status_code == 200
    assert response.text == "nothing more than text..."

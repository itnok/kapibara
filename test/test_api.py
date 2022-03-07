#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TEST api.py

"""

from errno import EINVAL
from sys import maxsize as sys_maxsize
from random import seed as rnd_seed
from random import randint as rnd_randint
from fastapi import status
from fastapi.testclient import TestClient

from app.kapibara.api import app
from app.kapibara.api import Kapibara
from app.kapibara.api import Kauthbara
from app.kapibara.__constants__ import __app_name__
from app.kapibara.__constants__ import __version__

import pytest

app.kauth = Kauthbara()
client = TestClient(app)


@pytest.mark.parametrize(
    "username,password,expected_response",
    [
        ("this-username-is-wrong-for-sure", "", False),
        (__app_name__, "this-is-the-wrong-password", False),
        (__app_name__, __app_name__, True),
    ],
)
def test_class_kauthbara_authenticate(username, password, expected_response):
    """[TEST] Class Kauthbara - authenticate
    """
    k = Kauthbara()
    assert k.authenticate(username=username,
                          password=password) == expected_response


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


def test_class_kapibara_server_port_gt_zero():
    """[TEST] Class Kapibara correctly check configuration data for the server port
    """
    k = Kapibara()
    k.conf["server"]["port"] = -1
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        k.sanitize_configuration()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == EINVAL


def test_class_kapibara_load_configuration_errors():
    """[TEST] Class Kapibara - load_configuration errors
    """
    k = Kapibara()
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        k.load_configuration("this-configuration-file-does-not-exist")
    assert pytest_wrapped_e.type == SystemExit
    assert "[Errno 2] No such file or directory" in str(pytest_wrapped_e.value)


def test_class_kapibara_sanitize_configuration_errors():
    """[TEST] Class Kapibara - sanitize_configuration errors
    """
    k = Kapibara()
    k.conf.pop("server", None)
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        k.sanitize_configuration()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == EINVAL


def test_openapi_schema():
    """[TEST] OpenAPI schema is exposed correctly
    """
    response = client.get("/openapi.json")
    assert response.status_code == status.HTTP_200_OK, response.text


def test_get_root():
    """[TEST] get_root
    """
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == {"msg": ["Hello World!", __app_name__, __version__]}


def test_get_plaintext():
    """[TEST] get_plaintext
    """
    response = client.get("/plaintext")
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.text == "nothing more than text..."


def test_post_token():
    """[TEST] post_token
    """
    response = client.post("/token", data={
        "grant_type": "password",
        "username": __app_name__,
        "password": __app_name__,
    })
    assert response.status_code == status.HTTP_200_OK, response.text
    json_with_time_insensitive_token_chunk = response.json()
    print(json_with_time_insensitive_token_chunk["access_token"])
    json_with_time_insensitive_token_chunk["access_token"] = \
        ".".join(json_with_time_insensitive_token_chunk["access_token"].split(".", 2)[:2])[:-8]
    print(json_with_time_insensitive_token_chunk["access_token"])
    assert json_with_time_insensitive_token_chunk == {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHAiOiJrYXBpYmFyYSIsImV4cCI6MTY0NjY",
            "token_type": "bearer",
        }


#
#   Mock data for test_post_token_errors
#
required_params = {
    "detail": [
        {
            "loc": ["body", "grant_type"],
            "msg": "field required",
            "type": "value_error.missing",
        },
        {
            "loc": ["body", "username"],
            "msg": "field required",
            "type": "value_error.missing",
        },
        {
            "loc": ["body", "password"],
            "msg": "field required",
            "type": "value_error.missing",
        },
    ]
}

grant_type_required = {
    "detail": [
        {
            "loc": ["body", "grant_type"],
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]
}

grant_type_incorrect = {
    "detail": [
        {
            "loc": ["body", "grant_type"],
            "msg": 'string does not match regex "password"',
            "type": "value_error.str.regex",
            "ctx": {"pattern": "password"},
        }
    ]
}

@pytest.mark.parametrize(
    "data,expected_status,expected_response",
    [
        (None, status.HTTP_422_UNPROCESSABLE_ENTITY, required_params),
        (
            {"username": "johndoe", "password": "secret"},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            grant_type_required
        ),
        (
            {"username": "johndoe", "password": "secret", "grant_type": "incorrect"},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            grant_type_incorrect,
        ),
        (
            {"username": "johndoe", "password": "secret", "grant_type": "password"},
            status.HTTP_401_UNAUTHORIZED,
            {"msg": "Incorrect username or password"},
        ),
    ],
)
def test_post_token_errors(data, expected_status, expected_response):
    """[TEST] post_token (All error conditions)
    """
    response = client.post("/token", data=data)
    assert response.status_code == expected_status
    assert response.json() == expected_response


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
        response = client.get(f"/items/{random_id}",
                              params=params[i],
                              headers={"Authorization": "Bearer footokenbar"})
        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.json() == (
            {"item_id": random_id, "q": params[i]["q"]}
            if params[i] else
            {"item_id": random_id, "q": None})


def test_get_items_forbidden():
    """[TEST] get_items (401 - Not Authenticated)
    """
    response = client.get("/items/0")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text
    assert response.json() == {"msg": "Not authenticated"}


def test_get_items_validation():
    """[TEST] get_items (422 - Validation error)
    """
    response = client.get("/items/string",
                          headers={"Authorization": "Bearer footokenbar"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text

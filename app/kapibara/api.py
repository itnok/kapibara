#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""API stub

"""

from os import (
    getenv as os_getenv,
    getcwd as os_getcwd,
    path as os_path,
)
from sys import (
    exit as sys_exit,
    stderr as sys_stderr,
    version_info as sys_version_info,
)
from typing import (
    Dict,
    Optional,
)
from errno import (
    EINVAL,
    ENOTRECOVERABLE,
)
from logging import (
    getLogger as l_getLogger,
    Formatter as l_Formatter,
    FileHandler as l_FileHandler,
    StreamHandler as l_StreamHandler,
    DEBUG as l_DEBUG,
    ERROR as l_ERROR,
    INFO as l_INFO,
)
from colorlog import (
    ColoredFormatter as l_ColorFormatter,
)
from pydantic import (
    BaseModel,
)
from schema import (
    Schema,
    SchemaError,
    And as SchemaAnd,
    Optional as SchemaOpt,
)
from dotenv import (
    load_dotenv as dotenv_load,
)
try:
    from yaml import (
        load as yml_load,
        CLoader as yml_Loader,
    )
except ImportError: #pragma: no cover
    from yaml import (
        load as yml_load,
        yml_Loader,
    )
from fastapi import (
    FastAPI,
    status,
)
from fastapi.responses import (
    JSONResponse,
    PlainTextResponse,
)
from starlette.exceptions import (
    HTTPException as StarletteHTTPException,
)

from .__constants__ import (
    __app_name__,
    __description__,
    __version__,
)
from .shared.useful import (
    find_config_path,
)


__all__ = (
    "asgi",
    "Kapibara",
)


if sys_version_info < (3, 6, 0):    #pragma: no cover
    sys_stderr.write(
        "Python 3.6.x or newer is needed to run this script\n")
    sys_exit(ENOTRECOVERABLE)


#
# Expected schema for the configuration dictionary
#
_CONFIG_SCHEMA_ = Schema(
    {
        "server": {
            "addr": SchemaAnd(str),
            "port": SchemaAnd(int),
        },
        SchemaOpt("debug"): SchemaAnd(bool),
    },
    ignore_extra_keys=True
)


#
# Logging configuration
#
log = l_getLogger(__app_name__)
# Logging on disk in the current working directory (ERROR)
_log_disk_handler = l_FileHandler(os_path.join(os_getcwd(), f"{__app_name__}.log"))
_log_disk_handler.setLevel(l_ERROR)
_log_disk_format = l_Formatter("%(asctime)s - [%(levelname)s] %(message)s")
_log_disk_handler.setFormatter(_log_disk_format)
log.addHandler(_log_disk_handler)
# Logging on STDOUT (INFO)
_log_console_handler = l_StreamHandler()
_log_console_handler.setLevel(l_INFO)
_log_console_format = l_ColorFormatter("%(log_color)s[%(levelname)-8s] %(message)s%(reset)s")
_log_console_handler.setFormatter(_log_console_format)
log.addHandler(_log_console_handler)


#
# FastAPI static configuration
#
__tags_metadata__ = [
    {
        "name": "common",
        "description": "Endpoints of general used common to the whole API.",
    },
    {
        "name": "items",
        "description": "Operations involving the items.",
    },
]

app = FastAPI(title=__app_name__,
              version=__version__,
              openapi_tags=__tags_metadata__)


#pragma EXCEPTION: Exceptionbara
class Exceptionbara(Exception): #pragma: no cover
    """Class representing the Kapibara custom exception.

    :param name: Exception details
    :type name: str

    """
    __slots__ = {
        "__detail",
    }

    def __init__(self, detail: str):
        self.__detail = detail
        super().__init__(self.__detail)


#pragma MODEL: msgbara
class Msgbara(BaseModel):
    """Class representing the data model for the generic API response message.

    """
    msg: str


#pragma CLASS: Kapibara
class Kapibara:
    """[SINGLETON] Class to manage the Kapibara configuration.

    The class follows the singlteon pattern, but could be expandend
    to eventually provided other necessary underpinnings.

    :param name: Instance name
        defaults to `__app_name__`
    :type name: str, optional

    """
    __slots__ = {
        "__conf",
        "__name",
    }

    _instance = None

    def __new__(cls) -> object:
        """Constructor class method

        This method is the first to be used at the creation of a new instance of a class

        :return: The freshly created instance of Kapibara
        :rtype: Kapibara

        """
        if not cls._instance:
            cls._instance = super(Kapibara, cls).__new__(cls)
        return cls._instance

    def __init__(self, name: Optional[str] = __app_name__):
        """Constructor method

        """
        try:
            len(self.__name)
        except AttributeError:
            #
            #   This makes sure the __init__ method is
            #   NOT reused on an instance twice!
            #
            self.__name = name
            self.__conf = {
                "server": {
                    "addr": "localhost",
                    "port": 0,
                },
                "debug": False,
            }
            self.__conf = self.load_configuration(self.__name)
            if self.__conf["debug"]:    #pragma: no cover
                _log_console_handler.setLevel(l_DEBUG)
                _log_disk_handler.setLevel(l_DEBUG)
                log.setLevel(l_DEBUG)
            self.sanitize_configuration()

    @staticmethod
    def load_environment_variables(cnf: Dict) -> Dict:
        """Load environment variables eventually present to overwrite a configuration.

        It expects and returns the configuration as a Dict with the following schema:

            conf = {
                "server": {
                    "addr": "localhost",
                    "port": 0,
                },
                "debug": False,
            }

        The environment variables should have a name that _"depicts"_ the hierarchy of the
        configuration YAML file _(see :py:meth:`~Kapibara.load_configuration`)_.
        For instance:

            - :py:`{"server": {"addr": "localhost"}}`
              becomes :bash:`SERVER_ADDR="localhost"`

        :staticmethod:

        :param cnf: configuration dictionary
        :type cnf: Dict

        :return: The configuration
            Following the schema above
        :rtype: Dict
        """
        cnf["server"]["addr"] = \
            os_getenv("SERVER_ADDR",
                      default=cnf["server"]["addr"])
        cnf["server"]["port"] = \
            int(os_getenv("SERVER_PORT",
                          default=cnf["server"]["port"]))
        cnf["debug"] = \
            os_getenv("DEBUG",
                      default=str(cnf["debug"])).lower() \
            in ("true", "t", "1", "yes", "y")
        return cnf

    @property
    def conf(self) -> Dict:
        """
        Whole configuration dictionary.

        :getter: Returns the configuration
        :type: dict
        """
        return self.__conf

    @property
    def is_debug(self) -> bool: #pragma: no cover
        """
        Is in DEBUG mode?.

        :getter: Returns whether in DEBUG mode or not
        :type: bool
        """
        return self.__conf["debug"]

    @property
    def server_addr(self) -> str:   #pragma: no cover
        """
        Address the API server is bound to.

        :getter: Returns the bind address
        :type: str
        """
        return self.__conf["server"]["addr"]

    @property
    def server_port(self) -> int:   #pragma: no cover
        """
        Port the API server is listening to.

        :getter: Returns the listening port
        :type: int
        """
        return self.__conf["server"]["port"]

    def load_configuration(self, fname: str) -> Dict:
        """Load the configuration from the specified YAML file.

        It expects the YAML file to be named like the script and
        to be in the same directory as the script.
        The YAML file is expected to follow the schema:

            ---
            server:
                addr: "localhost"
                port: 8088

        :param fname: configuration file name
        :type fname: str

        :return: The configuration
            Following the schema presented in the input YAML file
            merged to the expected one _(see: :py:meth:`~Kapibara.load_environment_variables`)_
        :rtype: Dict
        """
        conf_file = os_path.join(find_config_path(f"{fname}.yml"), f"{fname}.yml")
        try:
            with open(conf_file, "r", encoding="utf-8") as file:
                configuration = yml_load(file, Loader=yml_Loader)
        except FileNotFoundError as err:
            log.critical(
                "Missing configuration file '%s'", conf_file)
            sys_exit(err)
        log.debug("load_configuration: %s", configuration)
        return Kapibara.load_environment_variables({**self.__conf, **configuration})

    def sanitize_configuration(self):
        """Sanitize the configuration making sure it adhere to the expected schema.

        When the configuration is not respecting the expected schema
        or eventually the data is not in the desired format,
        it forces the script to exit with a critical error.
        """
        try:
            _CONFIG_SCHEMA_.validate(self.__conf)
        except SchemaError as err:
            log.critical(
                "Configuration file content was not in the expected format: %s", err)
            sys_exit(EINVAL)
        if self.__conf["server"]["port"] <= 0:
            log.critical(
                "Server port to listen to must be greater than 0")
            sys_exit(EINVAL)


def asgi() -> FastAPI:  #pragma: no cover
    """Configure FastAPI app as needed and returns its instance

    This function is used when the FastAPI app needs to be imported
    from a different module/script _(e.g. for ``uvicorn``)_

    :return: Instance of FastAPI app
    :rtype: FastAPI
    """
    dotenv_load(os_path.join(find_config_path(f".env-{__app_name__}"), f".env-{__app_name__}"))
    app.kapi = Kapibara()
    return app


@app.exception_handler(StarletteHTTPException)
async def kapibara_exception_handler(exception: StarletteHTTPException):
    """Custom exceptions handler

    This exception handler standardizes the responses so that even _"magic"_
    performed by FastAPI under the hood obeys and complies with the desired
    documented format of error responses.
    Usually error status codes, using default FastAPI HTTPException, are paired
    with a `detail` field inside a JSON response. We want to keep the JSON response,
    but use the `msg` field to convey the human-readable state report.

    """
    return JSONResponse(status_code=exception.status_code,
                        content={"msg": exception.detail})


#    __ ___ _ __  _ __  ___ _ _
#   / _/ _ \ '  \| '  \/ _ \ ' \
#   \__\___/_|_|_|_|_|_\___/_||_|
#
#   #pragma TAG: common API endpoints
@app.get("/",
         tags=["common"],
         response_class=JSONResponse,
         responses={
            status.HTTP_200_OK: {
                "model": Msgbara,
                "description": "OK",
                "content": {
                    "application/json": {
                        "example": {"msg": ["Hello World!", __app_name__, __version__]},
                    },
                },
            },
         }
)
async def get_root():
    """[GET] / (async)

    Simple default 'application/json' request
    """
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"msg": ["Hello World!", __app_name__, __version__]})


@app.get("/plaintext",
         tags=["common"],
         response_class=PlainTextResponse
)
async def get_plaintext():
    """[GET] /plaintext (async)

    Simple 'text/plain' request
    """
    return PlainTextResponse(status_code=status.HTTP_200_OK,
                             content="nothing more than text...")


@app.get("/items/{item_id}",
         tags=["items"],
         response_class=JSONResponse,
)
async def get_item(item_id: int, q: Optional[str] = None):
    """[GET] /items/{item_id} (async)

    Simple 'application/json' request with option param
    """
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"item_id": item_id, "q": q})

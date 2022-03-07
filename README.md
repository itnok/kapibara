KAPIBARA
========

_FastAPI scaffolding to jump-start API development_

![KAPIBARA](asset/kapibara-hero.png)

---

[[_TOC_]]


---
## :pushpin: Requirements

`kapibara` is provided as a Python3 module and requires version 3.6.x or newer to be installed on the system.
It comes as a module to be easily re-used or integrated in a larger project, and it requires few other modules and programs it relays on.
The _(semi)_ automated installation process described in the following chapter also requires access to this repository _(it is not public just yet)_ and, in general, access to the Internet to download several publicly available packages.

The list of Python3 modules `kapibara` needs, is available as part of the `setup.cfg` configuration file _(more about this in the ["Developing" section](#wrench-developing) down below)_. The software is intended to be architecture independent, therefore it should run without any issue on any *NIX system like Linux, macOS or FreeBSD _(it is not intended, nor tested, to run on Windows... although, despite not being supported, it might work...)_.

To provide the service it is build for it also needs to be installed on a machine accessible via the network by a _(Docker)_ container Registry _(e.g. the one provided by any GitLab installation or the one available as a [stand alone container provided by Docker Hub as detailed in the "Testing" section](#test-tube-testing))_.


---
## :cloud: How To Install

There 3 different ways to download and use `kapibara` _(listed in order of decreasing preference)_:

- Clone this very repository: `git clone git@github.com:itnok/kapibara.git`
- Download using `pip`: `python3 -m pip install git+https://github.com/itnok/kapibara.git`
- Download a ready-to-use [Wheel _(see paragraph "Building The Wheel" for more info)_](#ferris-wheel-building-the-wheel) or tarball from the [Release page of this repository](https://github.com/itnok/kapibara/releases)

After downloading a Wheel it can be installed with:

```bash
$ python3 -m pip install \
    /path/to/some/kapibara-X.Y.Z-py3-none-any.wheel
```

After downloading a tarball it can be installed with:

```bash
$ python3 -m pip install \
    /path/to/some/kapibara-X.Y.Z.tar.gz
```


> ---
> :scroll: **Note:**
>
> Both Wheels and tarballs can also be downloaded and installed in one single command using `pip`, pointing it to the URL of the desired file.
>
> e.g.:
> ```bash
> $ python3 -m pip install \
>     https://github.com/itnok/kapibara/releases/download/X.Y.Z/kapibara-X.Y.Z.tar.gz
> ```
>
> ---


As a rule of thumb it is always recommended to install the package in a [separate Virtual Environment](https://docs.python.org/3/tutorial/venv.html), to make sure it is possible to have much strict control on the installed dependencies and to avoid creating conflicts with other software written in Python.

For further and more detailed information on how to deal with Python packages a good starting point is the [python.org official tutorial](https://packaging.python.org/tutorials/installing-packages/)


---
## :running: How To Use

`kapibara` needs some configuration to happen before being able to properly work:

1. Customize the `kapibara` configuration _([via `kapibara.yml` YAML file](#1-a-configuration-via-yaml-file) or providing [suitable Environment variables](#1-b-configuration-via-environment-variables))_

After the configuration phase it is ready to use/run and it provides a scaffolding to build a more articulated API ready to be distributed and/or containerized.

After launching the `kapibara` server, the documentation of all endpoint is automatically generated and available at the address `http://hostname:port/redoc`.

### 1.a Configuration via YAML file

`kapibara` can be configured via a YAML file with the following syntax:

```yaml
---
server:
    addr: "<address-to-bind-kapibara-server>"
    port: <tcp-port-to-listen-to>
crypt:
    key: "<put-your-secret-encryption-key-here>"

```

In the previous example the following conventions were adopted:

- anything enclosed in `"` _(double-quotes)_ is supposed to be a string
- anything not enclosed in double-quotes is supposed to be an integer
- anything enclosed in `<>` _(angular-brackets)_ is supposed to be a mandatory value
- anything enclosed in `[]` _(square-brackets)_ is supposed to be an optional value

An example of the YAML configuration file is also [available directly in the repository](https://github.com/itnok/kapibara/blob/master/kapibara.yml).

The configuration file `kapibara.yml` can be in any of the following locations _(they are going to be evaluated in the order listed)_:

- Directory where the `kapibara.py` script is saved _(usually `${VIRTUAL_ENV}/lib/python${PYTHON_VERSION}/site-packages/kapibara/` for Virtual Environments when installed as a Python Wheel)_
- Directory where the `kapibara.py` script is saved + `/.config` _(usually `${VIRTUAL_ENV}/lib/python${PYTHON_VERSION}/site-packages/kapibara/.config` for Virtual Environments when installed as a Python Wheel)_
- Current working directory _(the directory from where the command was issued)_
- `${HOME}/`
- `${HOME}/.config/kapibara/`
- `${HOME}/.config/`
- `${HOME}/.local/kapibara/`
- `${HOME}/.local/`
- `/etc/kapibara/`
- `/etc/`
- `<prefix>/share/kapibara` _(`<prefix>` is `${VIRTUAL_ENV}` for Virtual Environments)_
- `<prefix>/share/kapibara/.config/kapibara` _(`<prefix>` is `${VIRTUAL_ENV}` for Virtual Environments)_
- `<prefix>/share/kapibara/.config/` _(`<prefix>` is `${VIRTUAL_ENV}` for Virtual Environments)_

An example of a configuration:

```yaml
---
server:
    addr: "0.0.0.0"
    port: 8088
crypt:
    key: "Thi$-i5-5up3r$ecr37!!!"
```

Values in `kapibara.yml` can be overwritten [providing equivalent Environment variables as explained in the following paragraph](#1-b-configuration-via-environment-variables).


### 1.b Configuration via Environment Variables

`kapibara` can be configured also via Environment Variables. They can be sourced from the environment itself or provided via a `.env-kapibara` environment file. Whatever present in `.env-kapibara` has priority and overwrites eventually already configured Environment Variables.
Like [what happens for `kapibara.yml`](#1-a-configuration-via-yaml-file), environment file `.env-kapibara` can be in any of the following locations _(they are going to be evaluated in the order listed)_:

- Directory where the `kapibara.py` script is saved _(usually `${VIRTUAL_ENV}/lib/python${PYTHON_VERSION}/site-packages/kapibara/` for Virtual Environments when installed as a Python Wheel)_
- Directory where the `kapibara.py` script is saved + `/.config` _(usually `${VIRTUAL_ENV}/lib/python${PYTHON_VERSION}/site-packages/kapibara/.config` for Virtual Environments when installed as a Python Wheel)_
- Current working directory _(the directory from where the command was issued)_
- `${HOME}/`
- `${HOME}/.config/kapibara/`
- `${HOME}/.config/`
- `${HOME}/.local/kapibara/`
- `${HOME}/.local/`
- `/etc/kapibara/`
- `/etc/`
- `<prefix>/share/kapibara` _(`<prefix>` is `${VIRTUAL_ENV}` for Virtual Environments)_
- `<prefix>/share/kapibara/.config/kapibara` _(`<prefix>` is `${VIRTUAL_ENV}` for Virtual Environments)_
- `<prefix>/share/kapibara/.config/` _(`<prefix>` is `${VIRTUAL_ENV}` for Virtual Environments)_

The name of the supported Environment Variables can be obtained by looking and the schema of `kapibara.yml` separating each key in the YAML hierarchy with `_` _(underscore AKA low dash)_ and making the result upper case. For instance:

```yaml
---
server:
    addr: "0.0.0.0"

```

will become `SERVER_ADDR="0.0.0.0"`.

The full list of configurable Environment variable is therefore as follows:

```bash
SERVER_ADDR=""
SERVER_PORT=
CRYPT_KEY=""

```

An example configuration, similar to the one presented in the previous section, this time via `.env-kapibara` file would be:

```bash
SERVER_ADDR="0.0.0.0"
SERVER_PORT=8088
CRYPT_KEY="Thi$-i5-5up3r$ecr37!!!"

```

Environment variables always _"trump"_ the configuration provided via `kapibara.yml` _(the content of `.env-kapibara` has priority over what already provided in the Environment)_

Once the configuration is in place `kapibara` can be executed and it will listen on the provided `${SERVER_ADDR}:${SERVER_PORT}`.

More information on how to start the server in [the following chapter dedicated to `uvicorn`](#unicorn-uvicorn)

###  :unicorn: uvicorn

Despite the microservice can be executed with [_(`uvicorn`)_](https://www.uvicorn.org/) with eventually a reverse proxy such as `nginx` in front of it. In the current implementation of the service `server.py` script to start `kapibara` it is not include support for the `https` protocol _(using `uvicorn` does include it, though!)_ and the base assumption is the certificate will be terminated on the reverse proxy. This is _"fine"_ when the microservice is running using `uvicorn` for development and _"perfectly safe"_ when there is a `nginx` reverse proxy in front of it where the certificate is terminated _(eventually inside a dedicated container)_.

To run `kapibara` via `uvicorn` a specific dedicated `server.py` Python script is available in the repository, but it is not part of the distribution packing. It can also be run directly from the CLI with:

```bash
$ uvicorn \
    --host 0.0.0.0 \
    --port 8088 \
    --workers $(nproc 2>/dev/null || sysctl -n hw.physicalcpu) \
    'path.to.kapibara.api:app'

```

The previous command will make `uvicorn` listen on all interfaces on port 8088 and create enough workers to use all cores available to handle incoming requests. For deployment behind a reverse proxy it is advisable not to bind all interfaces, but just `localhost`. For example:

```bash
$ uvicorn \
    --host 127.0.0.1 \
    --port 8000 \
    --workers $(nproc 2>/dev/null || sysctl -n hw.physicalcpu) \
    'path.to.kapibara.api:app'

```

More information about how to deploy `uvicorn` using `nginx` please [follow the official documentation](https://www.uvicorn.org/deployment/#running-behind-nginx).


---
## :ferris_wheel: Building The Wheel

This module comes [ready to be eventually published to the public Python Package Index _(AKA PyPI)_](https://packaging.python.org/tutorials/packaging-projects/) and adopts an approach to limit the amount of places where versioning and package information should be edited. Instead of having all information repeated across different files _(`pyproject.toml`, `setup.cfg` and `setup.py`, among others)_, the metadata is harvested from `setup.cfg` by `setup.py` _(including this very `README.md` used as "long description" for the package)_. Data about the `__version__` and brief `__description__` of the package is automatically relayed into the module and available for programmatic evaluation shall the need arise.

The additional work done to prepare the package for inclusion in PyPI brings the advantage of providing a very quick way to build a [Python Wheel](https://pythonwheels.com/) eventually very useful to distribute the package and to make it much easier to use _(e.g. in the context of CI/CD)_. To build a wheel for this package, from the root of this repository use the following commands _(As always in Python, it is probably wise to do this operation inside an isolated virtual environment, nevertheless the `build` package should take care of this for you)_:

```bash
$ python3 -m pip install --upgrade build
$ python3 -m build

```

At the end of a successful build process a new directory `dist` is created and both a `tar.gz` archive and a Python Wheel are saved therein _(and can be used for distribution)_.


---
## :wrench: Developing

First step to contribute and develop features for `kapibara` is to clone the `git` repository _(currently the repository is not yet publicly available despite the MIT licensing)_:

```bash
$ git clone \
    git@github.com:itnok/kapibara.git

```

It is **strongly recommended** to create and activate a dedicated [Virtual Environment](https://docs.python.org/3/tutorial/venv.html) for it so that its dependencies do not interfere with the other Python packages installed system-wide _(also update `pip` to the latest version)_:

```bash
$ deactivate >/dev/null 2>&1 || true
$ python3 -m venv venv-kapibara
$ . venv-kapibara/bin/activate
$ python3 -m pip install --upgrade pip

```

Then the required dependencies should be installed. Because everything in the project is _"centralized"_ in the `setup.cfg` file _(to avoid duplication and the maintenance nightmare of updating the same data over different files)_, the _"usual"_ `requirements.txt` file is **intentionally missing**. Dependencies are automatically installed and sourced when `kapibara` is [installed using `pip` as a Wheel](#cloud-how-to-install), but for development they should be manually installed with:

```bash
$ ./install_requirements.py

```

<details>
<summary>Further options</summary>
<p>The same exact behavior can also be obtained with just <code>bash</code> <em>(arguably in a much more convoluted way)</em>:

```bash
$ TMP_REQ=$(mktemp -t kapibara.requirements); \
    cat setup.cfg \
    | tr '\n' ' ' \
    | grep -oE 'install_requires =(.*)zip_safe =' \
    | sed \
        -e 's~install_requires =~~g' \
        -e 's~zip_safe =~~g' \
        -e 's~  *~ ~g' \
    | tr ' ' '\n' \
    > ${TMP_REQ} \
    && \
    python3 -m pip install -r ${TMP_REQ}

```
</details>

For development and debugging purposes it is possible to activate a `DEBUG` mode _(this will set the logging level to a lower lever showing `log.debug` contents)_. To achieve that there are several options:

- Set an Environment Variable `DEBUG=YES`;
- Set the same variable as above in `.env-kapibara`
- Add one more root key to `kapibara.yml`:

```yaml
---
debug: yes

```

The `server.py` script also accept some command line arguments, and among others `--debug` will activate the debug mode _(`server.py` can be started as a CLI without directly using `uvicorn` as previously described in the ["How To Use --> :unicorn: uvicorn" section](#unicorn-uvicorn))_. For more information about the CLI arguments `server.py` supports:

```bash
$ python3 server.py --help

```

> ---
> :scroll: **Note:**
>
> If `pylint` is installed, it is supposed to return a value of `10/10` for all scripts part of the package!
>
> ---


---
## :test_tube: Testing

In the `test` directory are stored unit test files for `pytest` _(eventually supporting the `pytest-cov` plugin for coverage)_. Unit test files are aiming at providing full 100% coverage for the entire project, but even in this scaffolding the currently cover no more than 75% of the code base. Examples are provided for all API endpoints and for a subset of the functions and methods of the whole package. To run the test suite `pylint` needs to be installed:

```bash
$ python3 -m pip install pytest pytest-cov
$ pytest
```

Each run will also automatically perform coverage tests, equivalent to running:

```bash
$ pytest --cov=app
```

`pytest-cov` can generate better reporting in different formats. For more information refer directly to [its official documentation](https://pytest-cov.readthedocs.io/en/latest/).

Thanks to FastAPI the API is created automagically and it is accessible via web browser. All endpoints can be manually tested directly in the browser after the server is started _(more information in the [chapter dedicated to `uvicorn`](#unicorn-uvicorn))_ visiting `http://localhost:8088/docs`. The OpenAPI specification are also generated automatically and can be downloaded from `http://localhost:8088/openapi.json`. The file can then be used to configure other client applications _(e.g. [Postman](https://www.postman.com/) or [Paw](https://paw.cloud/))_.


---
## :lock: Authentication

The base scaffolding comes with a bare bones implementation of OAuth2.0 security using the `password` grant type to produce a Bearer Token used for one of the example endpoints. This is for the sake of simplicity and is present in the scaffolding for demonstration purpose only. [The `password` grant type is considered deprecated and disallowed by best current practice](https://oauth.net/2/grant-types/password/). Please make sure, in your final implementation of the API to implement a better strategy or leverage an external OAuth2.0 provider.


---
## :copyright: License

The software is released under the very liberal [MIT License](LICENSE).

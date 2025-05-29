# Friss Matcher

Takes information about two people and computes the probability that they are
the same individual. Use first name, last name, date of birth, and ID number to
apply matching logic and return a similarity score.

This exercise implements a `Python project` with the following features:

* [Django REST framework](https://www.django-rest-framework.org/) as the framework for building the API
* [uvicorn](https://www.uvicorn.org/) is our ASGI choice for production
* [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) for string matching
* some demonstrative unit tests with [pytest](https://pytest.org/)
* packaged using Python [wheel](https://pypi.org/project/wheel/)
* a command line interface using [argparse](https://docs.python.org/3/library/argparse.html)
* a docker machinery plus a makefile handler to allow running this project containerized
* some utilities as [Make](https://www.gnu.org/software/make/) commands


## Prerequisites

* [Python 3.9](https://www.python.org/)
* [pip](https://pypi.org/project/pip/)
* [Virtualenv](https://virtualenv.pypa.io/en/stable/)
* [Virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)
* [Make](https://www.gnu.org/software/make/)

Note: 
Our API example usages are done with the awesome [httpie](https://httpie.io/) tool.


## Standard Overview


### 1. Install this project

For manually installing and running the project you will need to:

```bash
# 1. Create & activate a virtualenv
mkvirtualenv -p python3.9 friss-matcher

# 2. Activate virtualenv (in case VE was not activated)
workon friss-matcher

# 3. Install package
python setup.py install
```


### 2. Check installation

Execute `friss-matcher`, the following *usage helper* should be
displayed:

```bash
usage: friss-matcher [-h] {manage,api} ...

positional arguments:
  {manage,api}
    manage      Run administrative tasks.
    api         Run API service.

optional arguments:
  -h, --help    show this help message and exit
```


### 3. Initialize the project

Run migrations:

```bash
friss-matcher manage migrate
```

Create a superuser `friss` with a password `123`:
```bash
friss-matcher manage createsuperuser
```

```bash
Username (leave blank to use 'user'): friss
Email address: 
Password: 
Password (again): 
This password is too short. It must contain at least 8 characters.
This password is too common.
This password is entirely numeric.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```


[comment]: <> (### 3. Lets run the project !)

[comment]: <> (This tool implements these subcommands:)

[comment]: <> ( * `api`)

[comment]: <> ( * `manage`)


### 4. Run the productive server

Launch the productive *ASGI* server with:

```bash
friss-matcher api
```

```bash
INFO:     Started server process [14728]
INFO:     Waiting for application startup.
INFO:     ASGI 'lifespan' protocol appears unsupported.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Note**: You need to set up Django with a productive web server, for example
[nginx](https://www.nginx.com/).

In another terminal, using *httpie* execute:

```bash
http localhost:8000/match/
```

The output should be:

```bash
HTTP/1.1 401 Unauthorized
Allow: POST, OPTIONS
Content-Length: 58
Content-Type: application/json
Referrer-Policy: same-origin
Vary: Accept, Cookie
WWW-Authenticate: Basic realm="api"
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
date: Sun, 21 Mar 2021 22:04:07 GMT
server: uvicorn

{
    "detail": "Authentication credentials were not provided."
}
```

Using our credentials:

```bash
http -a friss:123 POST localhost:8000/match/
```

Output:

```
HTTP/1.1 400 Bad Request
Allow: POST, OPTIONS
(...)
server: uvicorn

{
    "person_1": [
        "This field is required."
    ],
    "person_2": [
        "This field is required."
    ]
}
```

Stop the productive server with `ctrl-c`.


### 5. Run the development server

```bash
friss-matcher manage runserver 0.0.0.0:8000
```

In another terminal execute:

```bash
echo '{
    "person_1": {
        "first_name": "Andrew Craw",
        "last_name": "B",
        "bsn": "1"
    },
    "person_2": {
        "first_name": "Andrew Craw",
        "last_name": "B",
        "bsn": null
    }
}' | http -a friss:123 POST localhost:8000/match/
```

Result:

```bash
HTTP/1.1 200 OK
Allow: POST, OPTIONS
(...)
{
    "match": 60,
    "person_1": {
        "bsn": 1,
        "first_name": "Andrew Craw",
        "last_name": "B"
    },
    "person_2": {
        "bsn": 2,
        "first_name": "Andrew Craw",
        "last_name": "B"
    }
}
```


## Developer's Overview


### Build the library

```bash
python setup.py bdist_wheel
```

You will find the package at:

```bash
./dist/friss_matcher-1.0.0-py3-none-any.whl
```


### Running unit tests

```bash
# Inside our previously created virtualenv "friss-matcher"
pip install -r requirements-test.txt
pytest
```

Output:
```
============================ test session starts ============================
platform linux -- Python 3.9.2, pytest-6.2.2, py-1.10.0, pluggy-0.13.1
django: settings: friss_matcher.settings (from ini)
rootdir: /home/user/zfriss/friss-matcher, configfile: setup.cfg, testpaths: tests/
plugins: django-4.1.0, cov-2.11.1
collected 27 items

tests/friss_matcher/match/test_e2e.py ........                       [ 29%]
tests/friss_matcher/match/test_match.py ...................          [100%]

(...)

----------- coverage: platform linux, python 3.9.2-final-0 -----------
Name                                             Stmts   Miss  Cover
--------------------------------------------------------------------
src/friss_matcher/__init__.py                        0      0   100%
src/friss_matcher/__main__.py                       27     27     0%
src/friss_matcher/asgi.py                            4      4     0%
src/friss_matcher/cli.py                            13     13     0%
src/friss_matcher/definitions.py                     1      1     0%
src/friss_matcher/match/__init__.py                  0      0   100%
src/friss_matcher/match/admin.py                     1      1     0%
src/friss_matcher/match/apps.py                      4      4     0%
src/friss_matcher/match/migrations/__init__.py       0      0   100%
src/friss_matcher/match/models.py                   32      4    88%
src/friss_matcher/match/serializer.py               14      3    79%
src/friss_matcher/match/urls.py                      6      0   100%
src/friss_matcher/match/views.py                    13      1    92%
src/friss_matcher/settings.py                       25      0   100%
src/friss_matcher/urls.py                            3      0   100%
src/friss_matcher/wsgi.py                            4      4     0%
src/manage.py                                       12     12     0%
--------------------------------------------------------------------
TOTAL                                              159     74    53%

====================== 27 passed, 1 warning in 1.85s ========================
```

### Cleaning after a build execution

```bash
make clean
```

## Docker Overview

How to manipulate this project as a *dockerized application*.

### 1. Build docker image

Build the `friss-matcher` docker image need by the `api` service: 

```bash
docker-compose build api
```

Output:

```
Building api
Step 1/15 : FROM python:3.9-slim-buster as build
(...) 
Removing intermediate container 07e9c1b6f91d
 ---> afecd6e70d6f

Successfully built afecd6e70d6f
Successfully tagged friss-matcher:latest
```

### 2. Initialize the project

Our *docker compose* `api` service uses a volume `friss_data` in order to
persist information.

```bash
docker-compose run api friss-matcher manage migrate
```

```bash
Creating friss-matcher_api_run ... done
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
(...)
```

Create a superuser `friss` with a password `123`:
```bash
docker-compose run api friss-matcher manage createsuperuser
```

Output:

```bash
Creating friss-matcher_api_run ... done
Username (leave blank to use 'friss'): friss
Email address: 
Password: 
Password (again): 
This password is too short. It must contain at least 8 characters.
This password is too common.
This password is entirely numeric.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```


### 3. Start `api` service

Containerized *development* flavor server:

```bash
docker-compose up api
```

Containerized *production* flavor server:
```bash
docker-compose up api-prod
```

Observable output:

```
Creating friss-matcher_api-prod_1 ... done
Attaching to friss-matcher_api-prod_1
api-prod_1  | INFO:     Started server process [1]
api-prod_1  | INFO:     Waiting for application startup.
api-prod_1  | INFO:     ASGI 'lifespan' protocol appears unsupported.
api-prod_1  | INFO:     Application startup complete.
api-prod_1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

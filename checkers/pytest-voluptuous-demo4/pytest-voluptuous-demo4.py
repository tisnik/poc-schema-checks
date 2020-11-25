#!/usr/bin/env python
# vim: set fileencoding=utf-8

#
#  (C) Copyright 2018  Pavel Tisnovsky
#
#  All rights reserved. This program and the accompanying materials
#  are made available under the terms of the Eclipse Public License v1.0
#  which accompanies this distribution, and is available at
#  http://www.eclipse.org/legal/epl-v10.html
#
#  Contributors:
#      Pavel Tisnovsky
#

from pytest_voluptuous import S, Partial, Exact
from voluptuous import Invalid, Url, Any
from voluptuous.validators import All, Length
import requests
import re


def test_the_anything_endpoint_1():
    anything_struct = S(dict)
    response = requests.get("https://httpbin.org/anything").json()
    assert response == anything_struct


def test_the_anything_endpoint_2():
    anything_struct = S({"args": dict,
                         "data": str,
                         "files": dict,
                         "form": dict,
                         "headers": dict,
                         "json": None,
                         "method": str,
                         "origin": str,
                         "url": str})
    response = requests.get("https://httpbin.org/anything").json()
    assert response == anything_struct


def origin(value):
    if not re.fullmatch(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", value):
        raise Invalid("wrong input {i}, IP address expected".format(i=value))


def test_the_anything_endpoint_3():
    anything_struct = S({"args": dict,
                         "data": str,
                         "files": dict,
                         "form": dict,
                         "headers": S({str:str}),
                         "json": Any(None, str),
                         "method": Any("GET", "POST", "PUT", "DELETE"),
                         "origin": origin,
                         "url": Url()})

    response = requests.get("https://httpbin.org/anything").json()
    assert response == anything_struct

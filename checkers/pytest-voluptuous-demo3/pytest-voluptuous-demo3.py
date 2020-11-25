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
from voluptuous import Invalid
from voluptuous.validators import All, Length
from uuid import UUID
import requests


def uuid4(string):
    val = UUID(string, version=4)
    if val.hex != string.replace('-', ''):
        raise Invalid("the string '{s}' is not valid UUID4".format(s=string))


uuid_response_struct = S({"uuid": uuid4})


def test_uuid_1():
    assert {"uuid": "00ebf64b-c15e-4b5d-846a-28971dc05796"} == uuid_response_struct


def test_uuid_2():
    assert {"uuid": "00ebf64b-xxxx-4b5d-846a-28971dc05796"} == uuid_response_struct


def test_uuid_returned_by_the_service():
    response = requests.get("https://httpbin.org/uuid").json()
    assert response == uuid_response_struct

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

import sys
import traceback
from schemagic import validate_against_schema


def validate(schema, data):
    try:
        print("\n\n")
        print(schema)
        print(data)
        validate_against_schema(schema, data)
        print("pass")
    except (ValueError, TypeError) as e:
        print(e)


def is_type(value, expected_type):
    actual_type = type(value)
    if actual_type is not expected_type:
        msg = "Expected type: {expected}, but the value has type {actual}".format(
            expected=expected_type, actual=actual_type)
        raise TypeError(msg)


def is_int(value):
    is_type(value, int)


string_to_int_map = {str:is_int}

validate(string_to_int_map, {"prvni": 1, "druha": 2, "treti": 3})
validate(string_to_int_map, {"prvni": 1.5, "druha": "2", "treti": 3})
validate(string_to_int_map, {"prvni": "x", "druha": "y", "treti": "z"})
validate(string_to_int_map, {1: "x", 2: "y", 3: "z"})
validate(string_to_int_map, {1: 1, 2: 2, 3: 3})

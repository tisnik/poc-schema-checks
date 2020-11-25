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

import re
from sys import argv
from schema import Schema, SchemaError, And, Or, Optional, Regex


def validate(schema, data, verbose_mode=False):
    try:
        print("\n\n")
        if verbose_mode:
            print(schema)
        print(data)
        schema.validate(data)
        print("pass")
    except SchemaError as e:
        print(e)


def is_integer(value):
    return type(value) is int


def is_float(value):
    return type(value) is float


class Salary:
    def validate(self, value):
        if not is_integer(value) and not is_float(value):
            raise SchemaError("Salary has unexpected type {t}".format(t=type(value)))
        elif value <= 10000:
            raise SchemaError("Salary {s} is too low".format(s=value))
        elif value >= 99999.9:
            raise SchemaError("Salary {s} is too high".format(s=value))


class Position:
    POSITIONS = ["QA", "DevOps", "Admin", "Docs", "HR"]

    def validate(self, value):
        if value not in Position.POSITIONS:
            raise SchemaError("Unknown position '{p}'".format(p=value))


class UniqueId:

    def __init__(self):
        self._ids = set()

    def validate(self, value):
        if value in self._ids:
            raise SchemaError("ID {id} is not unique".format(id=value))
        self._ids.add(value)


employee = Schema({"name": And(str, len, Regex("[A-Z][a-z]+")),
                   "surname": And(str, len, Regex("[A-Z][a-z]+")),
                   "id": UniqueId(),
                   Optional("salary"): Salary(),
                   Optional("position"): And(str, Position())})

verbose_mode = "-v" in argv

validate(employee, {"name": "Eda",
                    "surname": "Wasserfall",
                    "id": 1,
                    "salary": 15000.0,
                    "position": "QA"},
                    verbose_mode)

validate(employee, {"name": "Eda",
                    "surname": "Wasserfall",
                    "id": 2,
                    "salary": 15000,
                    "position": "QA"},
                    verbose_mode)

validate(employee, {"name": "Eda",
                    "surname": "Wasserfall",
                    "id": 3,
                    "salary": -15000.0,
                    "position": "QA"},
                    verbose_mode)

validate(employee, {"name": "Eda",
                    "surname": "Wasserfall",
                    "id": 4,
                    "salary": 1000000.0,
                    "position": "QA"},
                    verbose_mode)

validate(employee, {"name": "Eda",
                    "surname": "Wasserfall",
                    "id": 5,
                    "salary": 15000.0,
                    "position": "QA"},
                    verbose_mode)

validate(employee, {"name": "Eda",
                    "id": 6,
                    "salary": 100000000.0,
                    "position": "QA"},
                    verbose_mode)

validate(employee, {"name": "Eda",
                    "surname": "Wasserfall",
                    "id": 7,
                    "salary": 45000.0,
                    "position": ""},
                    verbose_mode)

validate(employee, {"name": "Eda",
                    "surname": "Wasserfall",
                    "id": 8,
                    "salary": 45000.0,
                    "position": "tovarnik"},
                    verbose_mode)

validate(employee, {"name": "Eda",
                    "surname": "Wasserfall",
                    "id": 9,
                    "salary": 25000.0},
                    verbose_mode)

validate(employee, {"name": "Eda",
                    "surname": "Wasserfall",
                    "id": 10,
                    "position": "DevOps"},
                    verbose_mode)

validate(employee, {"name": "Eda",
                    "surname": "Wasserfall",
                    "id": 11},
                    verbose_mode)

validate(employee, {"id": 12},
                    verbose_mode)

validate(employee, {"name": "eda",
                    "surname": "Wasserfall",
                    "id": 13,
                    "salary": 45000.0,
                    "position": "HR"},
                    verbose_mode)

validate(employee, {"name": "Eda",
                    "surname": "wasserfall",
                    "id": 14,
                    "salary": 45000.0,
                    "position": "HR"},
                    verbose_mode)

validate(employee, {"name": "Eda",
                    "surname": "Unique",
                    "id": 1,
                    "salary": 45000.0,
                    "position": "HR"},
                    verbose_mode)

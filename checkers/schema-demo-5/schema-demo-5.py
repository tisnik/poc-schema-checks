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
from schema import Schema, SchemaError, And, Or, Optional


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


def positive_integer(value):
    return type(value) is int and value > 0


def positive_float(value):
    return type(value) is float and value > 0


def name_str(value):
    return re.fullmatch("[A-Z][a-z]+", value)


POSITIONS = ["QA", "DevOps", "Admin", "Docs", "HR"]

employee = Schema({"name": And(str, len, name_str),
                   "surname": And(str, len, name_str),
                   "id": positive_integer,
                   Optional("salary"): And(Or(positive_integer, positive_float), lambda x: x > 10000.0 and x < 99999.0),
                   Optional("position"): And(str, lambda s: s in POSITIONS)})

verbose_mode = "-v" in argv

validate(employee, {"name": "Eda",
                    "surname": "Wasserfall",
                    "id": 1,
                    "salary": 15000.0,
                    "position": "QA"},
                    verbose_mode)

validate(employee, {"name": "Eda",
                    "surname": "Wasserfall",
                    "id": 1,
                    "salary": 15000,
                    "position": "QA"},
                    verbose_mode)

validate(employee, {"name": "Eda",
                    "surname": "Wasserfall",
                    "id": 1,
                    "salary": -15000.0,
                    "position": "QA"},
                    verbose_mode)

validate(employee, {"name": "Eda",
                    "surname": "Wasserfall",
                    "id": 1,
                    "salary": 1000000.0,
                    "position": "QA"},
                    verbose_mode)

validate(employee, {"name": "Eda",
                    "surname": "Wasserfall",
                    "id": 1,
                    "salary": 15000.0,
                    "position": "QA"},
                    verbose_mode)

validate(employee, {"name": "Eda",
                    "id": 1,
                    "salary": 100000000.0,
                    "position": "QA"},
                    verbose_mode)

validate(employee, {"name": "Eda",
                    "surname": "Wasserfall",
                    "id": 1,
                    "salary": 45000.0,
                    "position": ""},
                    verbose_mode)

validate(employee, {"name": "Eda",
                    "surname": "Wasserfall",
                    "id": 1,
                    "salary": 45000.0,
                    "position": "tovarnik"},
                    verbose_mode)

validate(employee, {"name": "Eda",
                    "surname": "Wasserfall",
                    "id": 1,
                    "salary": 25000.0,},
                    verbose_mode)

validate(employee, {"name": "Eda",
                    "surname": "Wasserfall",
                    "id": 1,
                    "position": "DevOps"},
                    verbose_mode)

validate(employee, {"name": "Eda",
                    "surname": "Wasserfall",
                    "id": 1},
                    verbose_mode)

validate(employee, {"name": "eda",
                    "surname": "Wasserfall",
                    "id": 1,
                    "salary": 45000.0,
                    "position": "HR"},
                    verbose_mode)

validate(employee, {"name": "Eda",
                    "surname": "wasserfall",
                    "id": 1,
                    "salary": 45000.0,
                    "position": "HR"},
                    verbose_mode)

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

from voluptuous import Schema
from voluptuous import Invalid


def validate(schema, data):
    try:
        print("\n\n")
        print(schema)
        print(data)
        schema(data)
        print("pass")
    except Exception as e:
        print(e)


def pos(value):
    if type(value) is not int or value <= 0:
        raise Invalid("positive integer value expected, but got {v} instead".format(v=value))


number_list = Schema([int, float, complex])

validate(number_list, [1, 2, 3])
validate(number_list, [1.1, 2.2, 3.3])
validate(number_list, [1+2j, 3+4j, 5j])
validate(number_list, ["1", "2", "3"])

binary_numbers = Schema([0, 1])
validate(binary_numbers, [0, 0, 0])
validate(binary_numbers, [1, 1, 0])
validate(binary_numbers, [1, 2, 3])

validate(Schema(pos), 42)
validate(Schema(pos), 0)
validate(Schema(pos), -1)
validate(Schema(pos), 1.5)

user = Schema({"name": str,
               "surname": str,
               "id": pos})

validate(user, {"name": "Eda",
                "surname": "Wasserfall",
                "id": 1})

validate(user, {"name": "Eda",
                "id": 1})

validate(user, {"name": "Eda",
                "surname": "Wasserfall",
                "id": 0})

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

from schema import Schema, SchemaError


def validate(schema, data):
    try:
        print("\n\n")
        print(schema)
        print(data)
        schema.validate(data)
        print("pass")
    except SchemaError as e:
        print(e)


integer_list = Schema([int])
float_list = Schema([float])
string_list = Schema([str])

validate(integer_list, [1, 2, 3])
validate(integer_list, [1.1, 2.2, 3.3])
validate(integer_list, ["1", "2", "3"])

validate(float_list, [1, 2, 3])
validate(float_list, [1.1, 2.2, 3.3])
validate(float_list, ["1", "2", "3"])

validate(string_list, [1, 2, 3])
validate(string_list, [1.1, 2.2, 3.3])
validate(string_list, ["1", "2", "3"])

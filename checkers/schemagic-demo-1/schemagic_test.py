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
    except ValueError as e:
        print(e)
        traceback.print_exc(file=sys.stdout)


integer_list = [int]
string_list = [str]

validate(integer_list, [])
validate(integer_list, [1, 2, 3])
validate(integer_list, ["hello", "world", "!"])

validate(string_list, [])
validate(string_list, [1, 2, 3, 4])
validate(string_list, ["hello", "world", "!"])

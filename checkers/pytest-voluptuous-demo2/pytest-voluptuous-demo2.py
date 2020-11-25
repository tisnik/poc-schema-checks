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


def pos(value):
    if type(value) is not int or value <= 0:
        raise Invalid("positive integer value expected, but got {v} instead".format(v=value))


user = S({"name": str,
          "surname": str,
          "id": pos})


def test1():
    assert user == {"name": "Eda",
                    "surname": "Wasserfall",
                    "id": 1}


def test2():
    assert user == {"name": "Eda",
                    "id": 1}


def test3():
    assert user == {"name": "Eda",
                    "surname": "Wasserfall",
                    "id": 0}


users = S([S({"name": str,
             "surname": str,
             "id": pos})])

def test4():
    assert users == [{"name": "Eda",
                      "surname": "Wasserfall",
                      "id": 1},
                     {"name": "Varel",
                      "surname": "Frištenský",
                      "id": 2}]

def test5():
    assert users == [{"name": "Eda",
                      "surname": "Wasserfall",
                      "id": 0},
                     {"surname": "Frištenský",
                      "id": 2}]

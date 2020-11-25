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
from voluptuous.validators import All, Length

number_list = S([int, float, complex])


def test1():
    assert [1, 2, 3] == number_list
    assert [1, 2, 3.2] == number_list


def test2():
    assert [2j, 4j, 5j] == number_list
    assert [1+2j, 3+4j, 5j] == number_list


def test3():
    assert [1, "2", 3] == number_list


def test4():
    assert ["1", "2", "3"] == number_list


def test5():
    assert (1, 2, 3) == number_list


binary_numbers = S([0, 1])

def test6():
    assert binary_numbers == [0, 0, 0]
    assert binary_numbers == [1, 1, 0]


def test7():
    assert binary_numbers == [1, 2, 3]

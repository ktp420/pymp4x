#!/usr/bin/env python
"""
   Copyright 2016 beardypig

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import logging
import pytest

from pymp4.adapters import VarBytesInteger

log = logging.getLogger(__name__)

def to_bytes(a, order, signed):
    for x in range(11):
        try:
            return int(a).to_bytes(x, order, signed=signed)
        except OverflowError:
            pass


def from_big_to_little(bstr):
    return bstr[::-1]

## Big-endian Tests #######################################################

var_big_bytes_to_signed_int_data = [
    (-1*0xffffffffffffffff, b'\xff\x00\x00\x00\x00\x00\x00\x00\x01'),
    (-1*0xffffff, b'\xff\x00\x00\x01'), (-1*0x1000000, b'\xff\x00\x00\x00'),
    (-1*0xffff, b'\xff\x00\x01'), (-1*0x10000, b'\xff\x00\x00'),
    (-256, b'\xff\x00'), (-255, b'\xff\x01'), (-129, b'\xff\x7f'),
    (-128, b'\x80'), (0, b'\x00'),(127, b'\x7f'),
    (128, b'\x00\x80'), (255, b'\x00\xff'), (256, b'\x01\x00'),
    (0xffff, b'\x00\xff\xff'), (0x10000, b'\x01\x00\x00'),
    (0xffffff, b'\x00\xff\xff\xff'), (0x1000000, b'\x01\x00\x00\x00'),
    (0xffffffffffffffff, b'\x00\xff\xff\xff\xff\xff\xff\xff\xff'),
    (0x10000000000000000, b'\x01\x00\x00\x00\x00\x00\x00\x00\x00')
]
var_little_bytes_to_signed_int_data = [
    (a, from_big_to_little(expected))
    for a, expected in var_big_bytes_to_signed_int_data
]

#- Build tests ---------------------------------------------------------

@pytest.mark.parametrize("a,expected", var_little_bytes_to_signed_int_data)
def test_build_signed_int_from_var_little_endian_bytes(a, expected):
    i = VarBytesInteger(swapped=True).build(a)
    assert i == expected

@pytest.mark.parametrize("a,expected", var_big_bytes_to_signed_int_data)
def test_build_signed_int_from_var_big_endian_bytes(a, expected):
    i = VarBytesInteger().build(a)
    assert i == expected

#- Parse Tests ---------------------------------------------------------

@pytest.mark.parametrize("expected,a", var_little_bytes_to_signed_int_data)
def test_parse_signed_int_to_var_little_endian_bytes(a, expected):
    i = VarBytesInteger(signed=True, swapped=True).parse(a)
    assert i == expected

@pytest.mark.parametrize("expected,a", var_big_bytes_to_signed_int_data)
def test_parse_signed_int_to_var_big_endian_bytes(a, expected):
    i = VarBytesInteger(signed=True).parse(a)
    assert i == expected

## Little-endian Tests ##################################################

var_big_bytes_to_unsigned_int_data = [
    (0, b'\x00'), (128, b'\x80'), (254, b'\xfe'), (255, b'\xff'),
    (256, b'\x01\x00'), (0xffff, b'\xff\xff'),
    (0x10000, b'\x01\x00\x00'), (0xffffff, b'\xff\xff\xff'),
    (0x1000000, b'\x01\x00\x00\x00'), 
    (0xffffffffffffffff, b'\xff\xff\xff\xff\xff\xff\xff\xff'),
    (0x10000000000000000, b'\x01\x00\x00\x00\x00\x00\x00\x00\x00')
]
var_little_bytes_to_unsigned_int_data = [
    (a, from_big_to_little(expected))
    for a, expected in var_big_bytes_to_unsigned_int_data
]

#- Build tests ---------------------------------------------------------

@pytest.mark.parametrize("a,expected", var_little_bytes_to_unsigned_int_data)
def test_build_unsigned_int_from_var_little_endian_bytes(a, expected):
    i = VarBytesInteger(signed=False, swapped=True).build(a)
    assert i == expected

@pytest.mark.parametrize("a,expected", var_big_bytes_to_unsigned_int_data)
def test_build_unsigned_int_from_var_big_endian_bytes(a, expected):
    i = VarBytesInteger(signed=False, swapped=False).build(a)
    assert i == expected

#- Parse Tests ---------------------------------------------------------

@pytest.mark.parametrize("expected,a", var_little_bytes_to_unsigned_int_data)
def test_parse_unsigned_int_from_var_little_endian_bytes(a, expected):
    i = VarBytesInteger(signed=False, swapped=True).parse(a)
    assert i == expected

@pytest.mark.parametrize("expected,a", var_big_bytes_to_unsigned_int_data)
def test_parse_unsigned_int_from_var_big_endian_bytes(a, expected):
    i = VarBytesInteger(signed=False).parse(a)
    assert i == expected

#- Empty String Tests ---------------------------------------------------
def test_parse_signed_int_from_empty_bytes():
    a = b''
    i = VarBytesInteger(signed=True, swapped=True).parse(a)
    assert i == 0

def test_parse_unsigned_int_from_empty_bytes():
    a = b''
    i = VarBytesInteger().parse(a)
    assert i == 0

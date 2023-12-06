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

from pymp4.subconstructs import EmbeddableStruct, Embedded
from construct import Byte, Container, FixedSized, Struct, PaddedString, Pass

log = logging.getLogger(__name__)


def test_embedded_parse():
    obj = EmbeddableStruct("a"/Byte, Embedded(Struct("b"/Byte)), "c"/Byte).parse(b"abc")
    expected = Container(a=97, b=98, c=99)
    assert obj == expected

def test_embedded_build():                                                                              
    obj = EmbeddableStruct("a"/Byte, Embedded(Struct("b"/Byte)), "c"/Byte).build(
            Container(a=97, b=98, c=99))
    assert obj == b'abc'


invalid_embedds = [
    (PaddedString(2, "ascii"), Container(a=97, c=100)),
    (Pass, Container(a=97, c=98)),
    (Byte, Container(a=97, c=99)),
]

@pytest.mark.parametrize("data,expected", invalid_embedds)
def test_ignore_embedding_non_dict(data, expected):
    obj = EmbeddableStruct("a"/Byte, Embedded(data), "c"/Byte).parse(b"abcd")
    assert obj == expected

def test_nonparent_embedded_parse():
    obj = EmbeddableStruct("a"/Byte, Embedded(FixedSized(2, Struct("b"/Byte))), "c"/Byte).parse(b"abcd")
    expected = Container(a=97, b=98, c=100)
    assert obj == expected

def test_nonparent_embedded_build():
    obj = EmbeddableStruct("a"/Byte, Embedded(FixedSized(2, Struct("b"/Byte))), "c"/Byte).build(
            Container(a=97, b=98, c=99))
    assert obj == b'ab\x00c'

#!/usr/bin/env python
"""
   Copyright 2016-2019 beardypig

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
import unittest

from construct import Container, ListContainer

from pymp4.exceptions import BoxNotFound
from pymp4.util import BoxUtil

log = logging.getLogger(__name__)


class BoxTests(unittest.TestCase):
    box_data = Container(
        type="demo",
        children=ListContainer([
            Container(type="a   ", id=1),
            Container(type="b   ", id=2),
            Container(
                type="c   ",
                children=ListContainer([
                    Container(type="a   ", id=3),
                    Container(type="b   ", id=4),
                ])
            ),
            Container(type="d   ", id=5),
            Container(type="zzzz", id=100,
                children=ListContainer([
                    Container(type="zzzz", id=101),
                    Container(type="xyzz", id=102)
                ])
            ),
        ])
    )

    box_extended_data = Container(
        type="test",
        children=ListContainer([
            Container(
                type="a   ",
                id=1,
                extended_type=b"e--a"
            ),
            Container(
                type="b   ",
                id=2,
                extended_type=b"e--b"
            ),
            Container(
                type="c   ",
                id=3,
                extended_type=b"e--c",
                children=ListContainer([
                    Container(
                        type="d   ",
                        id=4,
                        extended_type=b"e--d"
                    )
                ])
            )
        ])
    )

    def test_child(self):
        self.assertListEqual(
            list(BoxUtil.child(self.box_data, "a   ")),
            [Container(type="a   ", id=1)]
        )

    def test_child_does_not_find_grand_child(self):
        self.assertListEqual(
            list(BoxUtil.child(self.box_data, "xyzz")),
            []
        )

    def test_child_missing(self):
        self.assertListEqual(
            list(BoxUtil.child(self.box_data, "NOTE")),
            []
        )

    def test_find(self):
        self.assertListEqual(
            list(BoxUtil.find(self.box_data, "b   ")),
            [Container(type="b   ", id=2), Container(type="b   ", id=4)]
        )

    def test_find_after_nest(self):
        self.assertListEqual(
            list(BoxUtil.find(self.box_data, "d   ")),
            [Container(type="d   ", id=5)]
        )

    def test_find_nested_type(self):
        self.assertListEqual(
            list(BoxUtil.find(self.box_data, "c   ")),
            [Container(type="c   ", children=ListContainer([
                Container(type="a   ", id=3),
                Container(type="b   ", id=4),
            ]))]
        )

    def test_find_empty(self):
        self.assertListEqual(
            list(BoxUtil.find(self.box_data, "f   ")),
            []
        )

    def test_first(self):
        self.assertEqual(
            BoxUtil.first(self.box_data, "b   "),
            Container(type="b   ", id=2)
        )

    def test_first_missing(self):
        self.assertRaises(
            BoxNotFound,
            BoxUtil.first, self.box_data, "f   ",
        )

    def test_find_extended(self):
        self.assertListEqual(
            list(BoxUtil.find_extended(self.box_extended_data, b"e--d")),
            [Container(type="d   ", id=4, extended_type=b"e--d")]
        )

    def test_find_extended_child(self):
        self.assertListEqual(
            list(BoxUtil.find_extended(self.box_extended_data, b"e--a")),
            [Container(type="a   ", id=1, extended_type=b"e--a")]
        )

    def test_index(self):
        self.assertEqual(
            BoxUtil.index(self.box_data, "b   "),
            1
        )

    def test_index_not_found(self):
        self.assertEqual(
            BoxUtil.index(self.box_data, "NOTE"),
            None
        )

    def test_index_no_childrens(self):
        self.assertEqual(
            BoxUtil.index(Container(type="NOTE", id=1), "NOTE"),
            None
        )

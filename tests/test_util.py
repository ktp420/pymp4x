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

    box_search_data = Container(
        type=b"demo",
        children=ListContainer([
            Container(type=b"a   ", id=1),
            Container(type=b"b   ", id=2),
            Container(
                type=b"c   ",
                children=ListContainer([
                    Container(type="a   ", id=3),
                    Container(type=b"b   ", id=4),
                    Container(type=b"\xa9too", id=99),
                    Container(type=b"c   ", id=98),
                ])
            ),
            Container(type=b"d   ", id=5),
            Container(type="zzzz", id=100,
                entries=ListContainer([
                    Container(type=b"zzzz", id=101),
                    Container(type="xyzz", id=102)
                ])
            ),
        ])
    )

    def test_search_convert_to_bytes_false(self):
        actual = list(BoxUtil.search(self.box_data, "a   ", decode=False))
        expect = [Container(type="a   ", id=1), Container(type="a   ", id=3)]
        assert actual == expect

    def test_search_not_found(self):
        # convert_to_bytes true so "a   " converts to b"a   "
        actual = list(BoxUtil.search(self.box_data, "a   "))
        expect = []
        assert actual == expect

    def test_search(self):
        # convert_to_bytes true so "a   " converts to b"a   "
        actual = list(BoxUtil.search(self.box_search_data, "a   "))
        expect = [Container(type=b"a   ", id=1)]
        assert actual == expect

    def test_search_converts_bytes2bytes(self):
        # convert_to_bytes true so b"\xa9too" converts to b"\xa9to"
        actual = list(BoxUtil.search(self.box_search_data, b"\xa9too"))
        expect = [Container(type=b"\xa9too", id=99)]
        assert actual == expect

    def test_search_converts_str2bytes(self):
        # convert_to_bytes true so "\\xa9too" converts to b"\xa9too"
        actual = list(BoxUtil.search(self.box_search_data, "\\xa9too"))
        expect = [Container(type=b"\xa9too", id=99)]
        assert actual == expect

    def test_search_converts_utf8_str2bytes(self):
        # convert_to_bytes true so "\xa9too" converts to b"\xc2\xa9too"
        actual = list(BoxUtil.search(self.box_search_data, "\xa9too"))
        expect = []
        assert actual == expect

    def test_search_includes_childrens(self):
        # convert_to_bytes true so "b   " converts to b"b   "
        actual = list(BoxUtil.search(self.box_search_data, "b   ", decode=True))
        expect = [Container(type=b"b   ", id=2), Container(type=b"b   ", id=4)]
        assert actual == expect

    def test_search_includes_childrens_of_matched(self):
        # convert_to_bytes true so "c   " converts to b"c   "
        actual = list(BoxUtil.search(self.box_search_data, "c   ", decode=True))
        expect = [self.box_search_data.children[2], Container(type=b"c   ", id=98)]
        assert actual == expect

    def test_search_key_is_id(self):
        actual = list(BoxUtil.search(self.box_search_data, 2, 3, key='id', decode=False))
        expect = [Container(type=b"b   ", id=2), Container(type="a   ", id=3)]
        assert actual == expect

    def test_search_children_key_is_entries(self):
        actual = list(BoxUtil.search(self.box_search_data.children[-1], 'zzzz', children='entries'))
        expect = [Container(type=b"zzzz", id=101)]
        assert actual == expect

    def test_search_key_does_not_exist(self):
        # convert_to_bytes true so "a   " converts to b"a   "
        actual = list(BoxUtil.search(self.box_search_data, "a   ", key='NOTE'))
        expect = []
        assert actual == expect

    def test_search_childen_key_does_not_exist_in_root_box(self):
        # convert_to_bytes true so "a   " converts to b"a   "
        actual = list(BoxUtil.search(self.box_search_data, "a   ", children='entries'))
        expect = []
        assert actual == expect

    def test_search_empty_key_returns_self(self):
        actual = list(BoxUtil.search(self.box_search_data.children[0]))
        expect = [self.box_search_data.children[0]]
        assert actual == expect

    def test_search_none_key_returns_self(self):
        actual = list(BoxUtil.search(self.box_search_data.children[0], None))
        expect = [self.box_search_data.children[0]]
        assert actual == expect

    def test_search_empty_str_key_returns_self(self):
        actual = list(BoxUtil.search(self.box_search_data.children[0], ""))
        expect = [self.box_search_data.children[0]]
        assert actual == expect

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

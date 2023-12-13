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
import unittest

from construct import Container, ListContainer, StringError
from pymp4.parser import Box, MetadataListItemBox

log = logging.getLogger(__name__)


class MetadataTests(unittest.TestCase):
    def test_udta_meta_parse(self):
        self.assertEqual(
            Box.parse(b'\x00\x00\x00\x14udta\x00\x00\x00\x0cmeta\x00\x00\x00\x00'),
            Container(
                offset=0,
                type=b'udta',
                children=ListContainer([
                    Container(
                        offset=8,
                        type=b'meta',
                        version=0,
                        flags=0,
                        children=ListContainer(),
                        end=20)
                    ]),
                end=20)
            )

    def test_udta_meta_build(self):
        self.assertEqual(
            Box.build(Container(
                offset=0,
                type=b'udta',
                children=ListContainer([
                    Container(
                        offset=8,
                        type=b'meta',
                        version=0,
                        flags=0,
                        children=ListContainer(),
                        end=20)
                    ]),
                end=20)
            ),
            b'\x00\x00\x00\x14udta\x00\x00\x00\x0cmeta\x00\x00\x00\x00')

    def test_hdlr_parse(self):
        self.assertEqual(
            Box.parse(b'\x00\x00\x00!hdlr\x00\x00\x00\x00\x00\x00\x00\x00mdirappl\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
            Container(
                offset=0,
                type=b'hdlr',
                version=0,
                flags=0,
                handler_type=b'mdir',
                manufacturer=b'appl',
                name=u'',
                end=33)
            )

    def test_hdlr_build(self):
        self.assertEqual(
            Box.build(Container(
                offset=0,
                type=b'hdlr',
                version=0,
                flags=0,
                handler_type=b'mdir',
                manufacturer=b'appl',
                name=u'',
                end=33)
            ),
            b'\x00\x00\x00!hdlr\x00\x00\x00\x00\x00\x00\x00\x00mdirappl\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    def test_ilst_parse(self):
        self.assertEqual(
            Box.parse(b'\x00\x00\x00(ilst\x00\x00\x00 \xa9nam\x00\x00\x00\x18data\x00\x00\x00\x01\x00\x00\x00\x00my title'),
            Container(
                offset=0,
                type=b'ilst',
                children=ListContainer([
                    Container(
                        offset=8,
                        type=b'\xa9nam',
                        children=ListContainer([
                            Container(
                                offset=16,
                                type=b'data',
                                version=0,
                                flags=1,
                                locale=0,
                                data=u'my title',
                                end=40)
                        ]),
                        end=40),
                ]),
                end=40)
            )

    def test_hdlr_build(self):
        self.assertEqual(
            Box.build(Container(
                offset=0,
                type=b'ilst',
                children=ListContainer([
                    Container(
                        offset=8,
                        type=b'\xa9nam',
                        children=ListContainer([
                            Container(
                                offset=16,
                                type=b'data',
                                version=0,
                                flags=1,
                                locale=0,
                                data=u'my title',
                                end=40)
                        ]),
                        end=40),
                ]),
                end=40)
            ),
            b'\x00\x00\x00(ilst\x00\x00\x00 \xa9nam\x00\x00\x00\x18data\x00\x00\x00\x01\x00\x00\x00\x00my title')

    def test_metadata_data_from_box_parses_raw_box(self):
        self.assertEqual(
            Box.parse(b'\x00\x00\x00\x1ddata\x00\x00\x00\x01\x00\x00\x00\x00Lavf58.76.100'),
            Container(
                 offset=0,
                 type=b'data',
                 data=b'\x00\x00\x00\x01\x00\x00\x00\x00Lavf58.76.100',
                 end=29)
            )

    def test_non_ascii_parse(self):
        self.assertEqual(
            Box.parse(b'\x00\x00\x00%\xa9to \x00\x00\x00\x1ddata\x00\x00\x00\x01\x00\x00\x00\x00Lavf58.76.100'),
            Container(offset=0, type=b'\xa9to ', data=b'\x00\x00\x00\x1ddata\x00\x00\x00\x01\x00\x00\x00\x00Lavf58.76.100', end=37)
        )

    def test_metadata_list_item_parse(self):
        self.assertEqual(
            MetadataListItemBox.parse(b'\x00\x00\x00%\xa9too\x00\x00\x00\x1ddata\x00\x00\x00\x01\x00\x00\x00\x00Lavf58.76.100'),
            Container(
                offset=0,
                type=b'\xa9too',
                children=ListContainer([
                    Container(
                        offset=8,
                        type=b'data',
                        version=0,
                        flags=1,
                        locale=0,
                        data=u'Lavf58.76.100',
                        end=37)
                ]),
                end=37)
            )

    def test_metadata_list_item_build(self):
        self.assertEqual(
            MetadataListItemBox.build(Container(
                offset=0,
                type=b'\xa9too',
                children=ListContainer([
                    Container(
                        offset=8,
                        type=b'data',
                        version=0,
                        flags=1,
                        locale=0,
                        data=u'Lavf58.76.100',
                        end=27)
                ]),
                end=37)
            ),
            b'\x00\x00\x00%\xa9too\x00\x00\x00\x1ddata\x00\x00\x00\x01\x00\x00\x00\x00Lavf58.76.100')

    def test_box_using_metadata_list_parse(self):
        self.assertEqual(
            Box.parse(b'\x00\x00\x00\x82udta\x00\x00\x00zmeta\x00\x00\x00\x00\x00\x00\x00!hdlr\x00\x00\x00\x00\x00\x00\x00\x00mdirappl\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Milst\x00\x00\x00 \xa9nam\x00\x00\x00\x18data\x00\x00\x00\x01\x00\x00\x00\x00my title\x00\x00\x00%\xa9too\x00\x00\x00\x1ddata\x00\x00\x00\x01\x00\x00\x00\x00Lavf58.76.100'),
            Container(
                offset=0,
                type=b'udta',
                children=ListContainer([
                    Container(
                        offset=8,
                        type=b'meta',
                        version=0,
                        flags=0,
                        children=ListContainer([
                            Container(
                                offset=20,
                                type=b'hdlr',
                                version=0,
                                flags=0,
                                handler_type=b'mdir',
                                manufacturer=b'appl',
                                name=u'',
                                end=53),
                            Container(
                                offset=53,
                                type=b'ilst',
                                children=ListContainer([
                                    Container(
                                        offset=61,
                                        type=b'\xa9nam',
                                        children=ListContainer([
                                            Container(
                                                offset=69,
                                                type=b'data',
                                                version=0,
                                                flags=1,
                                                locale=0,
                                                data=u'my title',
                                                end=93)
                                        ]),
                                        end=93),
                                    Container(
                                        offset=93,
                                        type=b'\xa9too',
                                        children=ListContainer([
                                            Container(
                                                offset=101,
                                                type=b'data',
                                                version=0,
                                                flags=1,
                                                locale=0,
                                                data=u'Lavf58.76.100',
                                                end=130)
                                        ]),
                                        end=130),
                                ]),
                                end=130),
                        ]),
                        end=130),
                ]),
                end=130
            )
        )

    def test_box_using_metadata_list_build(self):
        self.assertEqual(
            Box.build(Container(
                offset=0,
                type=b'udta',
                children=ListContainer([
                    Container(
                        offset=8,
                        type=b'meta',
                        version=0,
                        flags=0,
                        children=ListContainer([
                            Container(
                                offset=20,
                                type=b'hdlr',
                                version=0,
                                flags=0,
                                handler_type=b'mdir',
                                manufacturer=b'appl',
                                name=u'',
                                end=53),
                            Container(
                                offset=53,
                                type=b'ilst',
                                children=ListContainer([
                                    Container(
                                        offset=61,
                                        type=b'\xa9nam',
                                        children=ListContainer([
                                            Container(
                                                offset=69,
                                                type=b'data',
                                                version=0,
                                                flags=1,
                                                locale=0,
                                                data=u'my title',
                                                end=93)
                                        ]),
                                        end=93),
                                    Container(
                                        offset=93,
                                        type=b'\xa9too',
                                        children=ListContainer([
                                            Container(
                                                offset=101,
                                                type=b'data',
                                                version=0,
                                                flags=1,
                                                locale=0,
                                                data=u'Lavf58.76.100',
                                                end=130)
                                        ]),
                                        end=130),
                                ]),
                                end=130),
                        ]),
                        end=130),
                ]),
                end=130
            )),
            b'\x00\x00\x00\x82udta\x00\x00\x00zmeta\x00\x00\x00\x00\x00\x00\x00!hdlr\x00\x00\x00\x00\x00\x00\x00\x00mdirappl\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Milst\x00\x00\x00 \xa9nam\x00\x00\x00\x18data\x00\x00\x00\x01\x00\x00\x00\x00my title\x00\x00\x00%\xa9too\x00\x00\x00\x1ddata\x00\x00\x00\x01\x00\x00\x00\x00Lavf58.76.100'
        )

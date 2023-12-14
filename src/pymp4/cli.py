#!/usr/bin/env python
from __future__ import print_function
import io
import logging
import argparse

from pymp4.parser import Box
from pymp4.util import BoxUtil, escape_decode
from construct import setGlobalPrintFullStrings

log = logging.getLogger(__name__)


def dump(args=None):
    parser = argparse.ArgumentParser(description='Dump all the boxes from an MP4 file')
    parser.add_argument("input_file", type=argparse.FileType("rb"), metavar="FILE", help="Path to the MP4 file to open")
    parser.add_argument("-f", "--full", action="store_true", default=True, help="Print all the data to console")
    parser.add_argument("-t", "--truncated", dest="full", action="store_false", help="Print truncated data to console")
    parser.add_argument("-b", "--box", action='append', required=False, help="Only dump given Box type(s)")

    args = parser.parse_args(args=args)

    setGlobalPrintFullStrings(args.full)

    boxes_to_dump = {escape_decode(b) for b in args.box or [] if b}

    fd = args.input_file
    fd.seek(0, io.SEEK_END)
    eof = fd.tell()
    fd.seek(0)

    while fd.tell() < eof:
        box = Box.parse_stream(fd)
        for b in BoxUtil.search(box, *boxes_to_dump, decode=False):
            print(b)

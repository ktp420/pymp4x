import pytest
import re

from pymp4 import cli

from pathlib import Path

TEST_FILE = str(Path(__file__).with_name('test.m4a'))

def test_missing_arg(capsys):
    with pytest.raises(SystemExit) as e:
        cli.dump(args=[])
    assert e.value.code == 2
    captured = capsys.readouterr()
    assert "the following arguments are required: FILE" in captured.err

def __assert_full_dump(capsys):
    captured = capsys.readouterr()
    assert "" == captured.err
    all_types = re.findall(r'type = [^\s]+', captured.out)
    assert all_types == ["type = b'ftyp'", "type = b'free'"]
    assert "major_brand = b'M4A ' " in captured.out
    assert captured.out.rstrip().endswith('end = 60')
    assert 'truncated,' not in captured.out

def test_dump(capsys):
    cli.dump(args=[TEST_FILE])
    __assert_full_dump(capsys)

def test_full_dump(capsys):
    cli.dump(args=['--full', TEST_FILE])
    __assert_full_dump(capsys)

def test_truncated_dump(capsys):
    cli.dump(args=['--truncated', TEST_FILE])
    captured = capsys.readouterr()
    assert "" == captured.err
    assert "major_brand = b'M4A ' " in captured.out
    assert captured.out.rstrip().endswith('end = 60')
    assert '\\x16\'... (truncated, total 24)' in captured.out

def __assert_free_box_only(capsys):
    captured = capsys.readouterr()
    assert "" == captured.err

    all_types = re.findall(r'type = [^\s]+', captured.out)
    assert all_types == ["type = b'free'"]

    assert "major_brand = b'M4A ' " not in captured.out
    assert "type = b'free'" in captured.out
    assert captured.out.rstrip().endswith('end = 60')
    assert "!\"#$' (total 24)" in captured.out

def test_dumping_specific_box(capsys):
    cli.dump(args=['-b', 'free', TEST_FILE])
    __assert_free_box_only(capsys)

def test_dumping_specific_box_with_escaped_input(capsys):
    cli.dump(args=['-b', '\\x66ree', TEST_FILE])
    __assert_free_box_only(capsys)

def test_dumping_specific_box_with_empty_string(capsys):
    cli.dump(args=['-b', '', TEST_FILE])
    __assert_full_dump(capsys)

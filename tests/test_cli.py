import pytest

from pymp4 import cli

from pathlib import Path

def test_missing_arg(capsys):
    with pytest.raises(SystemExit) as e:
        cli.dump(args=[])
    assert e.value.code == 2
    captured = capsys.readouterr()
    assert "the following arguments are required: FILE" in captured.err

def test_dump(capsys):
    test_file = str(Path(__file__).with_name('test.m4a'))
    cli.dump(args=[test_file])
    captured = capsys.readouterr()
    assert "" == captured.err
    assert "major_brand = u'M4A ' " in captured.out
    assert captured.out.rstrip().endswith('end = 36')

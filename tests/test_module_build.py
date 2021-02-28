import os
from py_build.main import main
import pytest
from subprocess import PIPE, run

def test_module_successful_build(capsys):
    # The following is like running `python -m py_build test -P tests.build_test`
    ret_code = main('tests.build_test', 'test')
    actual = capsys.readouterr().out.strip().split('\n')
    assert actual == [
        'Step 1',
        'hello, world',
        'bye',
        'Done',
        'Step 2',
        'bye, moon',
        'hello',
        'Done'
    ]
    assert ret_code == 0

def test_module_package_not_found(capsys):
    ret_code = main('bad.package', 'test')
    actual = capsys.readouterr().err.strip()
    assert ret_code == 1
    assert actual == 'Module `bad.package.test` not found'

def test_module_module_not_found(capsys):
    ret_code = main('tests.build_test', 'bad_module')
    actual = capsys.readouterr().err.strip()
    assert ret_code == 1
    assert actual == 'Module `tests.build_test.bad_module` not found'
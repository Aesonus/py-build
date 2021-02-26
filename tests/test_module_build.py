import os
import pytest
from subprocess import PIPE, run

def test_build():
    output = run([
        'python', '-m', 'py_build', 'test', '-D', 'tests.build_test'
    ], stdout=PIPE, text=True)
    actual = output.stdout.strip().split('\n')
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
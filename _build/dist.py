from py_build.funcs import print_step_name
from py_build import *
import functools
import subprocess

def build_steps(builder: Builder):
    step = builder.composed(builder.build_step(), print_step_name(), builder.capture_results(print))

    @builder.capture_results(print)
    def run(*args):
        return subprocess.run(args, stdin=subprocess.PIPE, text=True,).stdout

    @step
    def create_sdist():
        r = 1 / 0
        run(
            'python', 'setup.py', 'sdist'
        )
        return 'Created sdist'

    @step
    def create_wheel():
        run(
            'python', 'setup.py', 'bdist_wheel'
        )
        return 'Created wheel'

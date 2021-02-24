from py_build.funcs import output_step, output_step_result
from py_build import *
import functools
import subprocess

def build_steps(builder: Builder):
    step = builder.composed(builder.build_step(), output_step(), builder.capture_results(output_step_result))

    def run(*args):
        return subprocess.run(*args, capture_output=True, text=True,).stdout

    @step
    def create_sdist():
        print(run([
            'python', 'setup.py', 'sdist'
        ]))
        return 'Created sdist'

    @step
    def create_wheel():
        print(run([
            'python', 'setup.py', 'bdist_wheel'
        ]))
        return 'Created wheel'

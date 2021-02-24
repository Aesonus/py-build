import argparse
from . import *
import importlib
import logging

parser = argparse.ArgumentParser("python -m " + name.split('/')[1], description='Runs the given build targets in order given')
parser.add_argument('target', nargs='+', help='Target or targets for the build action')
parser.add_argument('-D', '--directory', action='store', default='_build', help='Python package directory where the build files are found')
args = parser.parse_args()

for target in args.target:
    module = "{args.directory}.{target}".format(args=args, target=target)
    try:
        build_steps = importlib.import_module(module).build_steps
    except ModuleNotFoundError as ex:
        logging.error(' %s not found', ex.name)
        exit(1)
    except AttributeError as ex1:
        try:
            build_steps = importlib.import_module(module).Build
        except AttributeError as ex2:
            logging.error("%s", ex1.args[0])
            logging.error("%s", ex2.args[0])
            exit(1)

    builder = Builder()
    build_steps(builder)
    builder.build()
from py_build import Builder
import logging
import importlib

def main(directory: str, *targets) -> None:
    for target in targets:
        module = "{}.{}".format(directory, target)
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

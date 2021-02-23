from typing import Mapping, Optional


class _MetaBuilder(type):
    def __new__(cls, *args):
        c = super().__new__(cls, *args)
        c._steps = []
        c._executed_steps = 0
        return c

    @property
    def steps(self):
        return len(self._steps)

    @property
    def executed_steps(self):
        return self._executed_steps

class Builder(object, metaclass=_MetaBuilder):
    # TODO: Add default output_to and progress_to decorators

    @classmethod
    def build(cls, options: Optional[Mapping] = None):
        for fnc in cls._steps:
            try:
                fnc(**options)
            except TypeError:
                fnc()

    @classmethod
    def build_step(cls, func):
        """Counts each method decorated with this decorator"""
        def decorated(*args, **kwargs):
            cls._executed_steps += 1
            ret = func(*args, **kwargs)
            return ret
        cls._steps.append(decorated)
        return decorated

    @classmethod
    def output_to(cls, *args):
        """Calls each function in *args with the result of the decorated function"""
        output_functions = args
        def decorator(func):
            def decorated(*args, **kwargs):
                for arg in output_functions:
                    arg(func(*args, **kwargs))
            return decorated
        return decorator

    @classmethod
    def progress_to(cls, *args):
        """Calls each function in *args with the
        result of ```executed steps / steps```"""
        output_functions = args
        def decorator(func):
            def decorated(*args, **kwargs):
                ret = func(*args, **kwargs)
                for arg in output_functions:
                    arg(cls.executed_steps / cls.steps)
                return ret
            return decorated
        return decorator
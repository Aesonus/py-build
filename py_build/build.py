from typing import Callable, List, Mapping, Optional


class Builder(object):
    # TODO: Add default output_to and progress_to decorators

    def __init__(self) -> None:
        self._steps: List[Callable[..., str]] = []
        self._executed_steps: int = 0

    @property
    def steps(self) -> int:
        return len(self._steps)

    @property
    def steps_list(self):
        return self._steps

    @property
    def executed_steps(self):
        return self._executed_steps

    def build(self, options: Optional[Mapping] = None) -> None:
        for fnc in self.steps_list:
            try:
                fnc(**options)
            except TypeError:
                fnc()

    def build_step(self, func: Callable[..., str]) -> Callable[..., str]:
        """Counts each method decorated with this decorator"""
        def decorated(*args, **kwargs):
            self._executed_steps += 1
            ret = func(*args, **kwargs)
            return ret
        self.steps_list.append(decorated)
        return decorated

    def output_to(self, *args: Callable[..., str]) -> Callable[..., str]:
        """Calls each function in *args with the result of the decorated function"""
        output_functions = args

        def decorator(func):
            def decorated(*args, **kwargs):
                for arg in output_functions:
                    arg(func(*args, **kwargs))
            return decorated
        return decorator

    def progress_to(self, *args: Callable[..., str]) -> Callable[..., str]:
        """Calls each function in *args with the
        result of ```executed steps / steps```"""
        output_functions = args

        def decorator(func):
            def decorated(*args, **kwargs):
                ret = func(*args, **kwargs)
                for arg in output_functions:
                    arg(self.executed_steps / self.steps)
                return ret
            return decorated
        return decorator

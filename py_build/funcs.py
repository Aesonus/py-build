from typing import Callable
import functools
def output_step_result(output):
    print(output)

def output_step():
    def output_step(func: Callable):
        print(func.__name__.replace('_', ' ').capitalize() + '...')
        return func
    return output_step
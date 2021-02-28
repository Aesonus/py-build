"""
Runs mypy and tests when files are changed
"""

from typing import Dict
from watchdog.observers import polling
from watchdog import events
import subprocess
import time
import platform
import pathlib
import datetime

from watchdog.observers.api import DEFAULT_OBSERVER_TIMEOUT

def ci_actions() -> Dict[str, subprocess.CompletedProcess]:
    ret = {}
    if platform.system() == 'Windows':
        interpereter = pathlib.PurePath('env', 'Scripts', 'python.exe')
    elif platform.system() == 'Linux':
        pass
    coverage_file = pathlib.PurePath('build', 'coverage.xml')
    ret.update({'mypy': subprocess.run(
        [interpereter, '-m', 'mypy', '-m', 'py_build'], capture_output=True, text=True
    )})

    ret.update({'pytest': subprocess.run(
        [interpereter, '-m', 'pytest', 'tests'], capture_output=True, text=True
    )})
    return ret

class PyFileChangeHandler(events.PatternMatchingEventHandler):
    def on_any_event(self, event: events.FileSystemEvent):
        ret = ci_actions()
        if all((r.returncode == 0 for r in ret.values())):
            print('CI Success {:%I:%M}'.format(datetime.datetime.now()))
        else:
            print('CI Failed\n{}'.format("\n".join([k + ': ' + r.stdout for k, r in ret.items() if r.returncode != 0])))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', action='store_true')
    args = parser.parse_args()

    if args.run:
        ret = ci_actions()
        if all((r.returncode == 0 for r in ret.values())):
            exit(0)
        else:
            print('CI Checks Failed!\n{}'.format("\n".join([k + ': ' + r.stdout for k, r in ret.items() if r.returncode != 0])))
            exit(1)

    observer = polling.PollingObserver(timeout=3)
    observer.schedule(PyFileChangeHandler(ignore_directories=True, patterns=('*.py',), ignore_patterns='_build'), '.', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
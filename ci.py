"""
Runs mypy and tests when files are changed
"""

from watchdog import observers
from watchdog import events
import subprocess
import time

class PyFileChangeHandler(events.PatternMatchingEventHandler):
    def on_any_event(self, event: events.FileSystemEvent):
        print(event.src_path)
        print(event.event_type)
        subprocess.run(
            [
                'python', '-m', 'mypy', '-m', 'py_build'
            ]
        )
        subprocess.run(
            ['python', '-m', 'pytest']
        )

observer = observers.Observer(timeout=5)
observer.schedule(PyFileChangeHandler(ignore_directories=True, patterns=('*.py',)), '.', recursive=True)
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
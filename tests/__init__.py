"""Unit test package for pyspinner."""

import io
import sys


class CapturingSysOutput:
    """Capture data sended to sys.stdout
    """

    def __enter__(self):

        self._stdout = sys.stdout
        self._captured_output = io.StringIO()
        sys.stdout = self._captured_output
        self.result = None
        return self

    def __exit__(self, *args):
        self.result = self._captured_output.getvalue()
        del self._captured_output  # free up some memory
        sys.stdout = self._stdout

"""Main module."""

import time
import threading
import itertools

from functools import partial


class Spinner:

    _default_busy = False
    _default_delay = 0.3
    _default_chars = ("⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷")
    _default_delimiter = " "

    def __init__(
        self,
        init_text=None,
        delay=None,
        show_progress=None,
        progress_chars=None,
        delimiter=None,
        units_text=None,
    ):
        """"""
        self.init_text = init_text or "Working..."
        self.delay = delay or self._default_delay
        self.spinner_generator = itertools.cycle(progress_chars or self._default_chars)
        self.delimiter = delimiter or self._default_delimiter
        self.show_progress = show_progress
        self._updated_value = 0
        self._updated_tmpl = ""
        self._units_text = units_text or "items"

    def update(self, value):
        """"""
        try:
            self._updated_value += value
            if self.show_progress:
                self._updated_tmpl = (
                    f"Processed {self._updated_value} {self._units_text}"
                )
        except TypeError as exc:
            if "unsupported operand" in repr(exc):
                raise TypeError("`value` must be numeric, given %s" % type(value))
            raise

    def spinner_task(self):
        """"""
        p_print = partial(print, sep=self.delimiter, end="\r", flush=True)

        while self.busy:
            p_print(self.init_text, self._updated_tmpl, next(self.spinner_generator))
            time.sleep(self.delay)

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()
        return self

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False

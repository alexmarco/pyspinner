"""Main module."""

import time
import threading
import itertools

from functools import partial


class SpinnerError(Exception):
    pass


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
        units=None,
    ):
        """"""
        self.init_text = init_text or "Working..."
        self.show_delay = delay or self._default_delay
        self.spinner_generator = itertools.cycle(progress_chars or self._default_chars)
        self.delimiter = delimiter or self._default_delimiter
        self._units = units or "items"
        self._updated_value = 0
        self._updated_tmpl = ""
        self._thread = None
        self.show_progress = show_progress

    @property
    def show_delay(self):
        return self._show_delay

    @show_delay.setter
    def show_delay(self, value):
        """"""
        if not isinstance(value, (int, float)):
            raise SpinnerError(
                "`show_delay` value must be numeric, given %s" % type(value)
            )
        self._show_delay = value

    @property
    def show_progress(self):
        return self._show_progress

    @show_progress.setter
    def show_progress(self, value):
        """"""
        self._show_progress = value
        if value:
            self._updated_tmpl = "(processed {self._updated_value} %s" % self._units

    def update(self, value=None):
        """"""
        if not self._thread or not self._thread.is_alive():
            raise SpinnerError("Updatting value with no alive threads.")
        try:
            self._updated_value += value or 1
            self._progress_text = f"{self._updated_tmpl}"
        except TypeError as exc:
            if "unsupported operand" in repr(exc):
                raise TypeError("`value` must be numeric, given %s" % type(value))
            raise

    def spinner_task(self):
        """"""
        p_print = partial(print, sep=self.delimiter, end="\r", flush=True)

        while self._busy:
            p_print(self.init_text, self._updated_tmpl, next(self.spinner_generator))
            time.sleep(self._show_delay)

    @property
    def busy(self):
        return self._busy

    @property
    def thread(self):
        return self._thread

    def start(self):
        """"""
        if self._thread and self._thread.is_alive():
            raise SpinnerError("Exists alive spinner thread, stop first.")

        self._busy = True
        self._thread = threading.Thread(target=self.spinner_task)
        self._thread.start()
        return self._thread

    def stop(self):
        """"""
        if self._thread and self._thread.is_alive():
            self._busy = False
            self._thread.join(timeout=self._show_delay * 2)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exception, value, tb):
        self.stop()
        if exception is not None:
            return False

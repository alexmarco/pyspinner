#!/usr/bin/env python

"""Tests for `pyspinner` package."""
import time
import unittest

# from collections.abc import Generator

from pyspinner import Spinner
from pyspinner._core import SpinnerError

from _utils import CapturingSysOutput


class TestPyspinner(unittest.TestCase):
    """Tests for `pyspinner` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.maxDiff = None

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_instance(self):
        """Test something."""
        spi = Spinner()
        self.assertEqual(spi.init_text, "Working...")
        self.assertEqual(spi._updated_tmpl, "")

        spi.show_progress = True
        self.assertEqual(spi._updated_tmpl, "(processed {self._updated_value} items")
        with self.assertRaises(SpinnerError):
            spi.update()

    def test_run_01(self):
        """"""
        with CapturingSysOutput() as out:
            with Spinner():
                time.sleep(0.7)
        self.assertEqual(
            out.result.splitlines(), ["Working...  ⣾", "Working...  ⣽", "Working...  ⣻"]
        )

    def test_run_02(self):
        """"""
        with CapturingSysOutput() as out:
            with Spinner(init_text="Make awesome something..."):
                time.sleep(0.7)
        self.assertEqual(
            out.result.splitlines(),
            [
                "Make awesome something...  ⣾",
                "Make awesome something...  ⣽",
                "Make awesome something...  ⣻",
            ],
        )

    def test_run_03(self):
        """"""
        with CapturingSysOutput() as out:
            with Spinner(show_progress=True) as spi:
                for x in range(10):
                    spi.update()
                    time.sleep(0.2)
        for line in out.result.splitlines():
            self.assertRegex(line, r"Working...\s+(\(processed \d+ items\))?\W+")

    def test_run_04(self):
        """"""
        spi = Spinner()
        self.assertEqual(spi._thread, None)
        spi.start()
        time.sleep(0.1)
        self.assertEqual(spi._thread.is_alive(), True)
        spi.stop()
        self.assertEqual(spi._thread.is_alive(), False)
        spi.start()
        with self.assertRaises(SpinnerError):
            spi.start()
        spi.stop()

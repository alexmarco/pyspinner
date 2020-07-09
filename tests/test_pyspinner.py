#!/usr/bin/env python

"""Tests for `pyspinner` package."""
import time
import unittest

# from collections.abc import Generator

from pyspinner import Spinner

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
                    spi.update(1)
                    time.sleep(0.2)
        for line in out.result.splitlines():
            self.assertRegex(line, r"Working...\s+(\(processed \d+ items\))?\W+")

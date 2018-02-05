#!/usr/bin/env python3
import sys
import unittest
from collections import OrderedDict
from pathlib import Path


testsDir = Path(__file__).parent.absolute()
parentDir = testsDir.parent.absolute()

from kaitaiStructCompile import ChosenBackend, compile

inputDir = testsDir / "ksys"


class Test(unittest.TestCase):
	def testCompile(self):
		print("ChosenBackend", ChosenBackend)
		res = compile(inputDir / "a.ksy")
		self.assertEqual(len(res), 2)


if __name__ == "__main__":
	unittest.main()

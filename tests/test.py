#!/usr/bin/env python3

# run this from project root as `python -m tests.test`

import io
import unittest
from pathlib import Path

from ksykaitai import compile


testsDir = Path(__file__).parent.absolute()
inputDir = testsDir / "data"


class Test(unittest.TestCase):
	def testCompile(self):
		parser = compile(inputDir / "squashfs.ksy")
		self.assertEqual(parser.__name__, "SquashfsSuperblock")

	def testParse(self):
		parser = compile(inputDir / "squashfs.ksy")
		bindata = parser.from_file(inputDir / "snap.squashfs")
		self.assertEqual(bindata.superblock.inode_count, 3)

	def testDebug(self):
		compiled = Path('/tmp/ksycompiled.py')
		compiled.unlink(missing_ok=True)
		compile(inputDir / "squashfs.ksy", debug=True)
		self.assertTrue(compiled.is_file(), "Missing " + str(compiled))
		self.maxDiff = None
		self.assertMultiLineEqual(
				io.open(compiled).read(),
				io.open(inputDir / "squashfs_generated.py").read())


if __name__ == "__main__":
	unittest.main()

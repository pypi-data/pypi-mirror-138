# Builtin modules
import unittest
from typing import Any
from tempfile import TemporaryFile
# Third party modules
# Local modules
from .. import dump, dumps, load, loads, UnpackingError, PackingError
from ..fallback import (dump as pyDump, dumps as pyDumps, load as pyLoad, loads as pyLoads, UnpackingError as pyUnpackerError,
PackingError as pyPackerError)
# Program
class FSPackerTest(unittest.TestCase):
	dataVer1:Any = (
		None,
		True,
		False,
		0,
		-1,
		1,
		1<<256,
		0.0,
		0.1,
		-0.1,
		1.234e+16,
		1.234e-16,
		0.1000000000000001,
		float("inf"),
		float("-inf"),
		"",
		"test",
		"Ő",
		b'\xf0\xa4\xad\xa2'.decode(),
		b"",
		b"\x00",
		b"\x00FF00",
		tuple(),
		dict(),
		{"data":"ok"},
		{1:1},
		{(1,2,3):1},
		set(),
		set([1, "a", "test", "b", b"\x00"]),
		"F"*65000,
	)
	dataVer2:Any = (
		None,
		True,
		False,
		0,
		-1,
		1,
		1<<256,
		0.0,
		0.1,
		-0.1,
		1.234e+16,
		1.234e-16,
		0.1000000000000001,
		float("inf"),
		float("-inf"),
		"",
		"test",
		"Ő",
		"\\ua4ad",
		b'\xf0\xa4\xad\xa2'.decode(),
		b"",
		b"\x00",
		b"\x00FF00",
		tuple(),
		dict(),
		{"data":"ok"},
		{1:1},
		{(1,2,3):1},
		set(),
		set([1, "a", "test", "b", b"\x00"]),
		"F"*65000,
	)
	# VERSION 1
	def test_dumpsAndLoads_ver1(self) -> None:
		d:Any
		for d in self.dataVer1:
			self.assertEqual(loads(dumps( d, version=1)), (1, d))
			self.assertEqual(loads(pyDumps( d, version=1)), (1, d))
			self.assertEqual(pyLoads(pyDumps( d, version=1)), (1, d))
			self.assertEqual(pyLoads(dumps( d, version=1)), (1, d))
		self.assertTupleEqual(loads(dumps( self.dataVer1, version=1)), (1, self.dataVer1))
		self.assertTupleEqual(loads(dumps( (self.dataVer1, self.dataVer1), version=1 )), (1, (self.dataVer1, self.dataVer1)))
		self.assertTupleEqual(loads(dumps( [self.dataVer1, self.dataVer1], version=1 )), (1, (self.dataVer1, self.dataVer1)))
		self.assertTupleEqual(loads(dumps( {"data":self.dataVer1}, version=1 )), (1, {"data":self.dataVer1}))
		self.assertTupleEqual(pyLoads(pyDumps( self.dataVer1, version=1)), (1, self.dataVer1))
		self.assertTupleEqual(pyLoads(pyDumps( (self.dataVer1, self.dataVer1), version=1 )), (1, (self.dataVer1,self.dataVer1)))
		self.assertTupleEqual(pyLoads(pyDumps( [self.dataVer1, self.dataVer1], version=1 )), (1, (self.dataVer1,self.dataVer1)))
		self.assertTupleEqual(pyLoads(pyDumps( {"data":self.dataVer1}, version=1 )), (1, {"data":self.dataVer1}))
		return None
	def test_dumpAndLoad_ver1(self) -> None:
		with TemporaryFile() as fi:
			dump(self.dataVer1, fi, version=1)
			fi.flush()
			fi.seek(0)
			self.assertEqual(load(fi), (1, self.dataVer1))
			fi.seek(0)
			self.assertEqual(pyLoad(fi), (1, self.dataVer1))
			fi.seek(0)
			pyDump(self.dataVer1, fi, version=1)
			fi.flush()
			fi.seek(0)
			self.assertEqual(load(fi), (1, self.dataVer1))
			fi.seek(0)
			self.assertEqual(pyLoad(fi), (1, self.dataVer1))
		return None
	def test_packing_errors_ver1(self) -> None:
		with self.assertRaises(PackingError):
			dumps(range(2), version=1)
		with self.assertRaises(pyPackerError):
			pyDumps(range(2), version=1)
		with self.assertRaises(PackingError):
			dumps([[[1]]], version=1, recursiveLimit=2)
		with self.assertRaises(pyPackerError):
			pyDumps([[[1]]], version=1, recursiveLimit=2)
		with TemporaryFile() as fi:
			with self.assertRaises(PackingError):
				dump(range(2), fi, version=1)
			with self.assertRaises(pyPackerError):
				pyDump(range(2), fi, version=1)
			with self.assertRaises(PackingError):
				dump([[[1]]], fi, version=1, recursiveLimit=2)
			with self.assertRaises(pyPackerError):
				pyDump([[[1]]], fi, version=1, recursiveLimit=2)
		return None
	def test_unpacking_errors_ver1(self) -> None:
		d:bytes = dumps(self.dataVer1, version=1)
		with self.assertRaises(UnpackingError):
			loads(d[:-1])
		with self.assertRaises(pyUnpackerError):
			pyLoads(d[:-1])
		with self.assertRaises(UnpackingError):
			loads(b"\xff" + d[1:])
		with self.assertRaises(pyUnpackerError):
			pyLoads(b"\xff" + d[1:])
		d = dumps([0]*1024, version=1)
		with self.assertRaises(UnpackingError):
			loads(d, maxOPSize=512)
		with self.assertRaises(pyUnpackerError):
			pyLoads(d, maxOPSize=512)
		d = dumps(list(range(1024)), version=1)
		with self.assertRaises(UnpackingError):
			loads(d, maxDictSize=512)
		with self.assertRaises(pyUnpackerError):
			pyLoads(d, maxDictSize=512)
		with TemporaryFile() as fi:
			dump(self.dataVer1, fi, version=1)
			fi.flush()
			fi.seek(-1, 2)
			fi.truncate()
			fi.seek(0)
			with self.assertRaises(UnpackingError):
				load(fi)
			fi.seek(0)
			with self.assertRaises(pyUnpackerError):
				pyLoad(fi)
			dump(self.dataVer1, fi, version=1)
			fi.flush()
			fi.seek(0)
			fi.write(b"\xff")
			fi.seek(0)
			with self.assertRaises(UnpackingError):
				load(fi)
			fi.seek(0)
			with self.assertRaises(pyUnpackerError):
				pyLoad(fi)
		return None
	# VERSION 2
	def test_dumpsAndLoads_ver2(self) -> None:
		d:Any
		for d in self.dataVer2:
			self.assertEqual(loads(dumps( d, version=2)), (2, d))
			self.assertEqual(loads(pyDumps( d, version=2)), (2, d))
			self.assertEqual(pyLoads(pyDumps( d, version=2)), (2, d))
			self.assertEqual(pyLoads(dumps( d, version=2)), (2, d))
		self.assertTupleEqual(loads(dumps( self.dataVer2, version=2)), (2, self.dataVer2))
		self.assertTupleEqual(loads(dumps( (self.dataVer2, self.dataVer2), version=2 )), (2, (self.dataVer2, self.dataVer2)))
		self.assertTupleEqual(loads(dumps( [self.dataVer2, self.dataVer2], version=2 )), (2, (self.dataVer2, self.dataVer2)))
		self.assertTupleEqual(loads(dumps( {"data":self.dataVer2}, version=2 )), (2, {"data":self.dataVer2}))
		self.assertTupleEqual(pyLoads(pyDumps( self.dataVer2, version=2)), (2, self.dataVer2))
		self.assertTupleEqual(pyLoads(pyDumps( (self.dataVer2, self.dataVer2), version=2 )), (2, (self.dataVer2,self.dataVer2)))
		self.assertTupleEqual(pyLoads(pyDumps( [self.dataVer2, self.dataVer2], version=2 )), (2, (self.dataVer2,self.dataVer2)))
		self.assertTupleEqual(pyLoads(pyDumps( {"data":self.dataVer2}, version=2 )), (2, {"data":self.dataVer2}))
		return None
	def test_dumpAndLoad_ver2(self) -> None:
		with TemporaryFile() as fi:
			dump(self.dataVer2, fi, version=2)
			fi.flush()
			fi.seek(0)
			self.assertEqual(load(fi), (2, self.dataVer2))
			fi.seek(0)
			self.assertEqual(pyLoad(fi), (2, self.dataVer2))
			fi.seek(0)
			pyDump(self.dataVer2, fi, version=2)
			fi.flush()
			fi.seek(0)
			self.assertEqual(load(fi), (2, self.dataVer2))
			fi.seek(0)
			self.assertEqual(pyLoad(fi), (2, self.dataVer2))
		return None
	def test_packing_errors_ver2(self) -> None:
		with self.assertRaises(PackingError):
			dumps(range(2), version=2)
		with self.assertRaises(pyPackerError):
			pyDumps(range(2), version=2)
		with self.assertRaises(PackingError):
			dumps([[[1]]], version=2, recursiveLimit=2)
		with self.assertRaises(pyPackerError):
			pyDumps([[[1]]], version=2, recursiveLimit=2)
		with TemporaryFile() as fi:
			with self.assertRaises(PackingError):
				dump(range(2), fi, version=2)
			with self.assertRaises(pyPackerError):
				pyDump(range(2), fi, version=2)
			with self.assertRaises(PackingError):
				dump([[[1]]], fi, version=2, recursiveLimit=2)
			with self.assertRaises(pyPackerError):
				pyDump([[[1]]], fi, version=2, recursiveLimit=2)
		with TemporaryFile() as fi:
			with self.assertRaises(PackingError):
				dump(range(2), fi, version=2)
			with self.assertRaises(pyPackerError):
				pyDump(range(2), fi, version=2)
			with self.assertRaises(PackingError):
				dump([[[1]]], fi, version=2, recursiveLimit=2)
			with self.assertRaises(pyPackerError):
				pyDump([[[1]]], fi, version=2, recursiveLimit=2)
	def test_unpacking_errors_ver2(self) -> None:
		d:bytes = dumps(self.dataVer2, version=2)
		with self.assertRaises(UnpackingError):
			loads(d[:-1])
		with self.assertRaises(pyUnpackerError):
			pyLoads(d[:-1])
		with self.assertRaises(UnpackingError):
			loads(b"\xff" + d[1:])
		with self.assertRaises(pyUnpackerError):
			pyLoads(b"\xff" + d[1:])
		d = dumps([[[1]]], version=2)
		with self.assertRaises(UnpackingError):
			loads(d, recursiveLimit=2)
		with self.assertRaises(pyUnpackerError):
			pyLoads(d, recursiveLimit=2)
		with TemporaryFile() as fi:
			dump(self.dataVer2, fi, version=2)
			fi.flush()
			fi.seek(-1, 2)
			fi.truncate()
			fi.seek(0)
			with self.assertRaises(UnpackingError):
				load(fi)
			fi.seek(0)
			with self.assertRaises(pyUnpackerError):
				pyLoad(fi)
			dump(self.dataVer2, fi, version=2)
			fi.flush()
			fi.seek(0)
			fi.write(b"\xff")
			fi.seek(0)
			with self.assertRaises(UnpackingError):
				load(fi)
			fi.seek(0)
			with self.assertRaises(pyUnpackerError):
				pyLoad(fi)
		return None

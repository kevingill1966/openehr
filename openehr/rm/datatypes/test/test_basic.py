from openehr.rm.datatypes import basic
import unittest

class TestBoolean(unittest.TestCase):
    def test1(self):
        b1 = basic.DvBoolean(True)
        self.assertEqual(b1.value, True)
    def test2(self):
        b1 = basic.DvBoolean(False)
        self.assertEqual(b1.value, False)

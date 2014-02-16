from openehr.rm.datatypes import basic
import unittest

class TestDvBoolean(unittest.TestCase):
    def test1(self):
        b1 = basic.DvBoolean(True)
        self.assertEqual(b1.value, True)
    def test2(self):
        b1 = basic.DvBoolean(False)
        self.assertEqual(b1.value, False)
    def test3(self):
        t1 = basic.DvBoolean(True)
        self.assertEqual(t1, basic.DvBoolean.TRUE)
        f1 = basic.DvBoolean(False)
        self.assertEqual(f1, basic.DvBoolean.FALSE)
        self.assertNotEqual(basic.DvBoolean.TRUE, basic.DvBoolean.FALSE)

class TestDvIdentifier(unittest.TestCase):
    def test_construtor(self):
        i1 = basic.DvIdentifier('issuer', 'assigner', 'id', 'type')
        self.assertEqual(type(i1), basic.DvIdentifier)

        i2 = basic.DvIdentifier(i1)
        self.assertEqual(i1, i2)

        with self.assertRaises(AttributeError):
            i1 = basic.DvIdentifier(1, 2, 3, 4)

class TestDvState(unittest.TestCase):
    def test_construtor(self):
        i1 = basic.DvState(None, False)
        self.assertEqual(type(i1), basic.DvState)

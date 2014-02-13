
from openehr.rm.support import identification
import unittest

SECTIONS = [
        ["1.2.840.113554.1.2.2", "345"],
        ["1-2-840-113554-1", "789"],
        ["w123.com", "123"],
        ["1.2.840.113554.1.2.2", None],
        ["1-2-840-113554-1", None],
        ["w123.com", None]
    ]

STRING_VALUES = [
        "1.2.840.113554.1.2.2::345",
        "1-2-840-113554-1::789",
        "w123.com::123",
        "1.2.840.113554.1.2.2",
        "1-2-840-113554-1",
        "w123.com",
    ]

class TestHierObjectID(unittest.TestCase):

    def testConstructorTakesStringValue(self):
        for i, s in enumerate(STRING_VALUES):
            self.assertHOID(identification.HierObjectID(s), i)

    def testConstructorTakesSections(self):
        for i, s in enumerate(SECTIONS):
            self.assertHOID(identification.HierObjectID(s[0], s[1]), i)

    def assertHOID(self, hoid, i):
        self.assertEqual(STRING_VALUES[i], hoid.value)
        self.assertEqual(SECTIONS[i][0], hoid.root.value)
        self.assertEqual(SECTIONS[i][1], hoid.extension)

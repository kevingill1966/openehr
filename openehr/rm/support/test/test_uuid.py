
from openehr.rm.support import identification
import unittest

class TestUUID(unittest.TestCase):
    def testConstructorTakeString(self):
        self.assertNotEqual(identification.UUID("12888888-1444-1444-1244-15cccccccccc"), None)


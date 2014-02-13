
from openehr.rm.support import identification
import unittest

class TestUUID(unittest.TestCase):
    def testConstructorTakeString(self):
        self.assertNotEqual(identification.UUID("128-1-1-12-15"), None)


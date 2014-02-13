from openehr.rm.support import identification
import unittest
    
class TestISO_OID(unittest.TestCase):
    def testEquals(self):
        value = "1.2.840.113554.1.2.2"
        oid1 = identification.ISO_OID(value)
        oid2 = identification.ISO_OID(value)

        self.assertTrue(oid1 == oid2)
        self.assertTrue(oid2 == oid1)

        self.assertTrue(oid1 == oid1)
        self.assertTrue(oid2 == oid2)

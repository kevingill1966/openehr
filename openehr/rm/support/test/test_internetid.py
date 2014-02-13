from openehr.rm.support import identification
import unittest
    
class TestInternetID(unittest.TestCase):
    def testConstructorTakeString(self):
        self.assertNotEqual(None, identification.InternetID("www.google.com"))
        self.assertNotEqual(None, identification.InternetID("m-2.d2"))
        self.assertNotEqual(None, identification.InternetID("a123.com.nz"))
        self.assertNotEqual(None, identification.InternetID("openehr.org"))
        self.assertNotEqual(None, identification.InternetID("openehr1-1.org"))
        self.assertNotEqual(None, identification.InternetID("openehr1-1.com-2"))
        with self.assertRaises(identification.InvalidUID):
            identification.InternetID("128.17.13.1")
        with self.assertRaises(identification.InvalidUID):
            identification.InternetID("123.com")
        with self.assertRaises(identification.InvalidUID):
            identification.InternetID("open_ehr.org")
        with self.assertRaises(identification.InvalidUID):
            identification.InternetID("openehr1-.org")
        with self.assertRaises(identification.InvalidUID):
            identification.InternetID("openehr1-1.0")
        with self.assertRaises(identification.InvalidUID):
            identification.InternetID("openehr1-1.com.")

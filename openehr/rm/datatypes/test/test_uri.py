from openehr.rm.datatypes.uri import DvURI, DvEHRURI
import unittest

class TestDvURI(unittest.TestCase):
    def test_constructor(self):

        uri = DvURI("http://www.openehr.org")
        self.assertEqual(uri.scheme(), 'http')
        self.assertEqual(uri.path(), '/www.openehr.org')

        uri = DvURI("http://www.openehr.org/")
        self.assertEqual(uri.path(), '/www.openehr.org/')

        uri = DvURI("http://www.openehr.org/path1/path2/path3/")
        self.assertEqual(uri.path(), '/www.openehr.org/path1/path2/path3/')

        uri = DvURI('scheme://netloc/path;parameters?query#fragment')
        self.assertEqual(uri.scheme(), 'scheme')
        self.assertEqual(uri.path(), '/netloc/path;parameters')
        self.assertEqual(uri.query(), 'query')
        self.assertEqual(uri.fragments_id(), 'fragment')

    def test_equal(self):
        uri1 = DvURI("http://www.openehr.org/path1/path2/path3/")
        uri2 = DvURI("http://www.openehr.org/path1/path2/path3/")
        uri3 = DvURI("http://www.openehr.org/path1/path2/path3")
        self.assertEqual(uri1, uri2)
        self.assertNotEqual(uri1, uri3)

    def test_assignment(self):
        uri1 = DvURI("http://www.openehr.org/path1/path2/path3/")
        uri3 = DvURI("http://www.openehr.org/path1/path2/path3")
        self.assertNotEqual(uri1, uri3)
        uri3.value = DvURI("http://www.openehr.org/path1/path2/path3/")
        self.assertEqual(uri1, uri3)

        uri3.value = "http://www.openehr.org/path1/path2/path3"
        self.assertNotEqual(uri1, uri3)
        uri3.value = "http://www.openehr.org/path1/path2/path3/"
        self.assertEqual(uri1, uri3)

class TestDvEHRURI(unittest.TestCase):
    def test_constructor(self):
        DvEHRURI("ehr://www.openehr.org")
        with self.assertRaises(AttributeError):
            DvEHRURI("http://www.openehr.org")

    def test_invariant(self):
        uri = DvEHRURI("ehr://www.openehr.org")
        with self.assertRaises(AttributeError):
            uri.value = "http://www.openehr.org"

        uri.value = "ehr://www.openehr.org"
        uri.value = DvEHRURI("ehr://www.openehr.org")
        uri.value = DvURI("ehr://www.openehr.org")

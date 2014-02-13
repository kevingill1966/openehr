from openehr.rm.support.identification import ObjectRef, HierObjectID
import unittest
    
class TestObjectRef(unittest.TestCase):
    def testConstructor(self):
        with self.assertRaises(AttributeError):
            ObjectRef(None, "LOCAL", "EHR")

        with self.assertRaises(AttributeError):
            ObjectRef(HierObjectID("1.2.40.11.1.2.2::2"), None, "EHR")

        with self.assertRaises(AttributeError):
            ObjectRef(HierObjectID("1.2.40.11.1.2.2::2"), "LOCAL", None)

        oid = ObjectRef(HierObjectID("openehr.org::23"), "LOCAL", "EHR")

        self.assertEqual(oid.id, HierObjectID("openehr.org::23"))
        self.assertEqual(oid.namespace, "LOCAL")
        self.assertEqual(oid.type, "EHR")


    def testEquals(self):
        or1 = ObjectRef(HierObjectID("1-2-80-11-1"), "LOCAL", "EHR")
        or2 = ObjectRef(HierObjectID("1-2-80-11-1"), "LOCAL", "EHR")
        self.assertTrue(or1 == or2)
        self.assertTrue(or2 == or1)
        self.assertFalse(or1 != or2)
        self.assertFalse(or2 != or1)

        or3 = ObjectRef(HierObjectID("openehr.org::23"), "LOCAL", "EHR")
        self.assertFalse(or1 == or3)
        self.assertFalse(or3 == or1)
        self.assertTrue(or1 != or3)
        self.assertTrue(or3 != or1)

        or3 = ObjectRef(HierObjectID("1-2-80-11-1"), "DEMOGRAPHIC", "EHR")
        self.assertFalse(or1 == or3)
        self.assertFalse(or3 == or1)

        or3 = ObjectRef(HierObjectID("1-2-80-11-1"), "LOCAL", "PARTY")
        self.assertFalse(or1 == or3)
        self.assertFalse(or3 == or1)

from openehr.rm.support.identification import (ObjectVersionID, ISO_OID, HierObjectID,
    VersionTreeID, UUID, InternetID)
import unittest

class TestArchetypeID(unittest.TestCase):

    def testContructorTakeString1(self):
        idsets = [
            ["1.4.4.5", "1.2.840.114.1.2.2::123", "1"],
            ["1.2.4.5", "7234-235-422-4-23::2", "2.0.0"],
            ["1.6.1.6", "openehr.org::0.99", "2.1.2"]
        ]

        for i, idset in enumerate(idsets):
            ov = ObjectVersionID(idset[0], idset[1], idset[2])
            self.assertEqual(ISO_OID(idset[0]), ov.object_id())
            self.assertEqual(HierObjectID(idset[1]), ov.creating_system_id())
            self.assertEqual(VersionTreeID(idset[2]), ov.version_tree_id())

    def testContructorTakeString2(self):
        idsets = [
            ["1-4-4-5-12", "1.2.840.114.1.2.2", "1"],
            ["12-14-1-1-9", "7234-235-422-4-23::23", "2.0.0"],
            ["1123-1-4-5457-7", "openehr.org", "2.1.2"]
        ]
        for i, idset in enumerate(idsets):
            ov = ObjectVersionID(idset[0], idset[1], idset[2])
            self.assertEqual(UUID(idset[0]), ov.object_id())
            self.assertEqual(HierObjectID(idset[1]), ov.creating_system_id())
            self.assertEqual(VersionTreeID(idset[2]), ov.version_tree_id())

    def testContructorTakeString3(self):
        idsets = [
            ["openehr", "1.2.840.114.1.2.2", "1"],
            ["openehrR1-0.org", "7234-235-422-4-23::23", "2.0.0"],
            #{"openehr.org.uk", "w123.55.155::ext1", "2.1.2"}
        ]
        for i, idset in enumerate(idsets):
            ov = ObjectVersionID(idset[0], idset[1], idset[2])
            self.assertEqual(InternetID(idset[0]), ov.object_id())
            self.assertEqual(HierObjectID(idset[1]), ov.creating_system_id())
            self.assertEqual(VersionTreeID(idset[2]), ov.version_tree_id())
    
    def testCreateWithValidUIDInHexFormat(self):
        value = "939cec48-d629-4a3f-89f1-28c573387680::" + \
                "10aec661-5458-4ff6-8e63-c2265537196d::1"
        ObjectVersionID(value)


from openehr.rm.support import identification
import unittest

STRING_VALUE = [
    "openehr-ehr_rm-section.physical_examination.v2",
    "openehr-ehr_rm-section.physical_examination-prenatal.v1",
    "hl7-rim-act.progress_note.v1",
    "openehr-ehr_rm-ENTRY.progress_note-naturopathy.draft"
]

SECTIONS = [
    ["openehr", "ehr_rm", "section", "physical_examination", None, "v2"],
    ["openehr", "ehr_rm", "section", "physical_examination", "prenatal", "v1"],
    ["hl7", "rim", "act", "progress_note", None, "v1"],
    ["openehr", "ehr_rm", "ENTRY", "progress_note", "naturopathy", "draft"]
]

AXES = [
    ["openehr-ehr_rm-section", "physical_examination", "v2"],
    ["openehr-ehr_rm-section", "physical_examination-prenatal", "v1"],
    ["hl7-rim-act", "progress_note", "v1"],
    ["openehr-ehr_rm-ENTRY", "progress_note-naturopathy", "draft"]
]

class TestArchetypeID(unittest.TestCase):
    def testConstructorTakesStringValue(self):
        for s in STRING_VALUE:
              aid = identification.ArchetypeID(s)
              self.assertEqual(type(aid), identification.ArchetypeID)

    def testConstructorTakesSections(self):
        for s in SECTIONS:
            aid = identification.ArchetypeID(*s)
            self.assertEqual(type(aid), identification.ArchetypeID)

    def testConstructorWithInvalidValue(self):
        data = [
            # rm entity part
            "openehr-ehr_rm.physical_examination.v2", # too less sections
            "openehr-ehr_rm-section-entry.physical_examination-prenatal.v1", # to many sections
            "openehr.ehr_rm-entry.progress_note-naturopathy.v2", # too many axes

            # domain concept part
            "openehr-ehr_rm-section.physical+examination.v2", # illegal char

            # version part
            "hl7-rim-act.progress_note.", # missing version
            "openehr-ehr_rm-entry.progress_note-naturopathy"  # missing version
        ]

        for s in data:
            with self.assertRaises(ValueError):
                aid = identification.ArchetypeID(s)

    def testEqualsIgnoreVersionID(self):
        base1 = "openehr-ehr_rm-section.physical_examination."
        base2 = "openehr-ehr_rm-section.simple_medication."

        # same base
        self.assertEqual(identification.ArchetypeID(base1, "v1"),
            identification.ArchetypeID(base1, "v1"))
        self.assertEqual(identification.ArchetypeID(base1, "v1"),
            identification.ArchetypeID(base1, "v2"))
        self.assertEqual(identification.ArchetypeID(base1, "v2"),
            identification.ArchetypeID(base1, "v1"))

        # different base
        self.assertNotEqual(identification.ArchetypeID(base1, "v1"),
            identification.ArchetypeID(base2, "v1"))
        self.assertNotEqual(identification.ArchetypeID(base1, "v1"),
            identification.ArchetypeID(base2, "v2"))
        self.assertNotEqual(identification.ArchetypeID(base1, "v2"),
            identification.ArchetypeID(base2, "v1"))


    def testBase(self):
        base = "openehr-ehr_rm-section.physical_examination"
        self.assertEqual(base, identification.ArchetypeID(base + ".v1").base)
        
    def testMultipleSpecialisation(self):
        aid = identification.ArchetypeID("openEHR-EHR-CLUSTER.exam-generic-joint.v1")
        sp = ["generic","joint"]            
        self.assertEqual(sp, aid.specialisation)

    def testWithConceptInSwedish(self):
        #/ Omvrdnadsanteckning
        with self.assertRaises(ValueError):
            aid = identification.ArchetypeID( "openEHR-EHR-CLUSTER.Omv\u00E5rdnadsanteckning.v1")

    def testArchetypeBase(self):
        aid = identification.ArchetypeID("openEHR-EHR-CLUSTER.exam.v1")
        self.assertEqual("openEHR-EHR-CLUSTER.exam", aid.base)
        
        aid = identification.ArchetypeID("openEHR-EHR-CLUSTER.exam-generic.v1")
        self.assertEqual("openEHR-EHR-CLUSTER.exam-generic", aid.base)
        
        aid = identification.ArchetypeID("openEHR-EHR-CLUSTER.exam-generic-joint.v1")
        self.assertEqual("openEHR-EHR-CLUSTER.exam-generic-joint", aid.base)
        

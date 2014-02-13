
from openehr.rm.support.identification import TerminologyID
import unittest

STRING_VALUE = [
    "snomed-ct",  "ICD9(1999)"
]

SECTIONS = [
    ["snomed-ct", None],
    ["ICD9", "1999"]
]

    
class TestTerminologyID(unittest.TestCase):

    def language(self):
        LANGUAGE = TerminologyID("language-test")
        CHARSET = TerminologyID("charset-test")
        SNOMEDCT = TerminologyID("snomedct-test")

    def testConstrcutorTakesStringValue(self):
        for i, s in enumerate(STRING_VALUE):
            tid = TerminologyID(s)
            self.assertEquals(s, tid.value)
            self.assertEquals(SECTIONS[i][0], tid.name())
            self.assertEquals(SECTIONS[i][1], tid.version_id())

    def testConstrcutorTakesNameVersion(self):
        for i, s in enumerate(STRING_VALUE):
            tid = TerminologyID(SECTIONS[i][0], SECTIONS[i][1])
            self.assertEquals(s, tid.value)
            self.assertEquals(SECTIONS[i][0], tid.name())
            self.assertEquals(SECTIONS[i][1], tid.version_id())
    
    def testEquals(self):
        id1 = TerminologyID("ICD9", "1999")
        id2 = TerminologyID("ICD9", "1999")
        self.assertTrue(id1 == id2)
        self.assertTrue(id2 == id1)

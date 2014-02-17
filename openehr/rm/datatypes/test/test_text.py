from openehr.rm.support.terminology import TerminologyService
from openehr.rm.support.identification import TerminologyID
from openehr.rm.datatypes.text import DvText, CodePhrase, DvCodedText, TermMapping, DvParagraph
import unittest

class TestDvText(unittest.TestCase):
    def testConstructor(self):
        lang = CodePhrase(TerminologyID("ISO_639-1"), "en")
        encoding = CodePhrase(TerminologyID("IANA_character-sets"), "UTF-8");

        DvText("value", language=lang, encoding=encoding, terminology_service=TerminologyService())

        # verify that both language and charset are optional
        DvText("value")

    def test_equality(self):
        self.assertEqual(DvText('value'), DvText('value'))
        self.assertNotEqual(DvText('value1'), DvText('value2'))

    def test_bad_constructor(self):
        
        with self.assertRaises(AttributeError):
            DvText(None)

        with self.assertRaises(AttributeError):
            DvText("bad value\r\n")

        with self.assertRaises(AttributeError):
            DvText("bad value\n")

        with self.assertRaises(AttributeError):
            DvText("bad value\r")

        with self.assertRaises(AttributeError):
            DvText("")
#   
#   These are tests from tthe java version - I don't unerstand yet what they are testing TODO
#   def test_create_with_null_encoding(self):
#       lang = CodePhrase(TerminologyID("ISO_639-1"), "en")
#       with self.assertRaises(AttributeError):
#           DvText("test", language=lang, encoding=None, terminology_service=TerminologyService())

#   def test_create_with_null_language(self):
#       encoding = CodePhrase(TerminologyID("IANA_character-sets"), "UTF-8");
#       with self.assertRaises(AttributeError):
#           dt = DvText("test", language=None, encoding=encoding, terminology_service=TerminologyService())

class TestDvCodedText(unittest.TestCase):
    def testCreateDvCodedTextWithMinimumParam(self):
        defining_code = CodePhrase("test terms", "12345")
        DvCodedText(defining_code, 'value')
    
    def testEquals(self):
        t1 = DvCodedText(CodePhrase("icd10", "123"), 'some text')
        t2 = DvCodedText(CodePhrase("icd10", "123"), 'some text')
        self.assertEqual(t1, t2)

class TermMappingTest(unittest.TestCase):

    def testShouldInitializeWithNullPurpose(self):
        tm = TermMapping(CodePhrase("icd10", "123"), self.match(), None)

    def testShouldInitializeWithValidPurpose(self):
        tm = TermMapping(CodePhrase("icd10", "123"), self.match(), self.purpose(), self.DummyTerminologyService(True))

    def testShouldNotInitializeWithInvalidPurpose(self):
        with self.assertRaises(AttributeError):
            TermMapping(CodePhrase("icd10", "123"), self.match(), self.purpose(), self.DummyTerminologyService(False))

    def match(self):
        return '<'

    def purpose(self):
        tid = TerminologyID('SNOMED-CT')
        cp = CodePhrase(tid, 'abc123')
        return DvCodedText(cp, 'abc123')

    class DummyTerminologyService(object):
        def __init__(self, returnValue):
            self.returnValue = returnValue

        def terminology(self, terminologyID):
            return self.DummyTerminologyAccess(self.returnValue)

        class DummyTerminologyAccess(object):

            def __init__(self, returnValue):
                self.returnValue = returnValue

            def has_code_for_group_id(self, groupId, code):
                return self.returnValue


class DvParagraphTest(unittest.TestCase):

    def test_constructor(self):
        tid = TerminologyID(u"SNOMED-CT(2003)")
        tid1 = TerminologyID(u"ISO_639-1")
        tid2 = TerminologyID(u"10646-1:1993")
        cpm = CodePhrase(tid,u"abc123")
        tm = TermMapping(cpm,u"=",None)
        cplang = CodePhrase(tid1,u"en")
        cpenc = CodePhrase(tid2,u"utf-8")
        #uri = DvUri(u"http://www.mlhim.org")
        uri = None  # TODO
        txt1 = DvText(u"Some really interesting text line 1.",[tm,],u"font-family:Arial",uri,cplang,cpenc)
        txt2 = DvText(u"Some really interesting text line 2.",[tm,],u"font-family:Arial",uri,cplang,cpenc)
        txt3 = DvText(u"Some really interesting text line 3.",[tm,],u"font-family:Arial",uri,cplang,cpenc)
        txt4 = DvText(u"Some really interesting text line 4.",[tm,],u"font-family:Arial",uri,cplang,cpenc)
        par = DvParagraph([txt1,txt2,txt3,txt4])
        self.assertEqual(type(par), DvParagraph)
        self.assertEqual(len(par.items), 4)
        self.assertEqual(par.items[0], txt1)
        self.assertEqual(par.items[1], txt2)
        self.assertEqual(par.items[2], txt3)
        self.assertEqual(par.items[3], txt4)

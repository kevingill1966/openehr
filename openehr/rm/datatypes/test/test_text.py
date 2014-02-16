from openehr.rm.support.terminology import TerminologyService
from openehr.rm.support.identification import TerminologyID
from openehr.rm.datatypes.text import DvText, CodePhrase
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

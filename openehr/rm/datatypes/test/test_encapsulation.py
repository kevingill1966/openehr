from openehr.rm.datatypes.encapsulated import DvMultimedia, DvParsable
from openehr.rm.datatypes.text import CodePhrase
from openehr.rm.datatypes.uri import DvURI
from openehr.rm.support.terminology import TerminologyService

import unittest

class TestDvMultimedia(unittest.TestCase):
    def test_constructor(self):
        # This creates an object referenced via a URL
        charset = CodePhrase("IANA_character-sets", "UTF-8")
        language = CodePhrase("ISO_3166-1","eN")
        alternateText = "alternate text"
        mediaType = CodePhrase("IANA_media-types", "text/plain")
        compressionAlgorithm = CodePhrase("openehr_compression_algorithms", "others")

        integrityCheck = bytes()

        integrityCheckAlgorithm = CodePhrase("openehr_integrity_check_algorithms", "SHA-1")
        thumbnail = None
        uri = DvURI("http://www.iana.org")
        data = bytes()

        # terminologyService = TerminologyService()
        # TODO: why does java version use ts

        dm = DvMultimedia(charset=charset, language=language, alternate_text=alternateText,
                media_type=mediaType, compression_algorithm=compressionAlgorithm,
                integrity_check=integrityCheck, integrity_check_algorithm=integrityCheckAlgorithm,
                thumbnail=thumbnail, uri=uri, data=data)

        self.assertEqual(type(dm), DvMultimedia)
        self.assertEqual(dm.language, language)
        self.assertEqual(dm.charset, charset)
        self.assertEqual(dm.size, 0)
        self.assertEqual(dm.alternate_text, alternateText)
        self.assertEqual(dm.media_type, mediaType)
        self.assertEqual(dm.compression_algorithm, compressionAlgorithm)
        self.assertEqual(dm.integrity_check, integrityCheck)
        self.assertEqual(dm.integrity_check_algorithm, integrityCheckAlgorithm)
        self.assertEqual(dm.thumbnail, thumbnail)
        self.assertEqual(dm.uri, uri)
        self.assertEqual(dm.data, data)

        self.assertEqual(dm.is_external(), True)
        self.assertEqual(dm.is_inline(), False)
        self.assertEqual(dm.is_compressed(), True)
        self.assertEqual(dm.has_integrity_check(), True)

class TestDvParsable(unittest.TestCase):
    def test_constructor(self):
        charset = CodePhrase("IANA_character-sets", "UTF-8")
        language = CodePhrase("ISO_3166-1","eN")

        dp = DvParsable('Some Action', 'proforma', charset=charset, language=language)

        self.assertEqual(type(dp), DvParsable)
        self.assertEqual(dp.language, language)
        self.assertEqual(dp.charset, charset)
        self.assertEqual(dp.size, 11)
        self.assertEqual(dp.formalism, 'proforma')
        self.assertEqual(dp.value, 'Some Action')

        self.assertEqual(dp.as_string(), 'Some Action')

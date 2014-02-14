from openehr.rm.support import terminology
from openehr.rm.support import identification
import unittest

class TestTerminology(unittest.TestCase):

    def test_openehr_terminology(self):
        ts = terminology.TerminologyService()
        openehr = ts.terminology('openehr')
        self.assertEqual(openehr.id(), identification.TerminologyID('openehr'))

        ac = openehr.all_codes()
        self.assertEqual(len(ac), 263)

        ids = terminology.OpenEHRTerminologyGroupIdentifiers

        for gid in [ ids.GROUP_ID_ATTESTATION_REASON,
            ids.GROUP_ID_AUDIT_CHANGE_TYPE,
            ids.GROUP_ID_COMPOSITION_CATEGORY,
            ids.GROUP_ID_EVENT_MATH_FUNCTION,
            ids.GROUP_ID_INSTRUCTION_STATES,
            ids.GROUP_ID_INSTRUCTION_TRANSITIONS,
            ids.GROUP_ID_NULL_FLAVOURS,
            ids.GROUP_ID_PARTICIPATION_FUNCTION,
            ids.GROUP_ID_PARTICIPATION_MODE,
            ids.GROUP_ID_PROPERTIES,
            ids.GROUP_ID_SETTING,
            ids.GROUP_ID_SUBJECT_RELATIONSHIP,
            ids.GROUP_ID_TERM_MAPPING_PURPOSE,
            ids.GROUP_ID_VERSION_LIFECYCLE_STATE]:

            cg = openehr.codes_for_group_id(gid)
            self.assertNotEqual(cg, None)

        groupid = ids.GROUP_ID_SUBJECT_RELATIONSHIP

        cg = openehr.codes_for_group_id(groupid)

        terminologyid = identification.TerminologyID('openehr')
        terminologyid2 = identification.TerminologyID('openehr2')

        self.assertTrue(openehr.has_code_for_group_id(groupid, 
            terminology.CodePhrase(terminologyid, '3')))
        self.assertFalse(openehr.has_code_for_group_id(groupid,
            terminology.CodePhrase(terminologyid, '99')))
        self.assertFalse(openehr.has_code_for_group_id(groupid,
            terminology.CodePhrase(terminologyid2, '3')))

        cg_by_name = openehr.codes_for_group_name('Subject Relationship', 'en')

        rubric = openehr.rubric_for_code(terminology.CodePhrase(terminologyid, '3'), 'en')
        self.assertEqual('foetus', rubric)

        #rubric = openehr.rubric_for_code('32', 'de')
        #self.assertEqual('Subjekt der Daten', rubric)

#   def test_vsab_terminology(self):
#       """A list of terminology identifiers is loaded from the XML file at startup"""
#       ts = terminology.TerminologyService()
#       self.assertTrue('BI98' in ts.terminology_identifiers())
#       self.assertFalse('NOTKNOWN' in ts.terminology_identifiers())


    def test_openehr_codeset(self):
        ts = terminology.TerminologyService()

        cs_status = ts.code_set('openehr_normal_statuses')

        ac = cs_status.all_codes()
        self.assertEqual(len(ac), 7)
        self.assertTrue(cs_status.has_code(ac[0]))

        with self.assertRaises(AttributeError):
            cs_status.has_code(ac[0].code_string)

        self.assertFalse(cs_status.has_code(
            terminology.CodePhrase(identification.TerminologyID('ISO_639-1'), 'de')))

        self.assertTrue(cs_status.has_lang(
            terminology.CodePhrase(identification.TerminologyID('ISO_639-1'), 'en')))
        self.assertFalse(cs_status.has_lang(
            terminology.CodePhrase(identification.TerminologyID('ISO_639-1'), 'de')))

        with self.assertRaises(AttributeError):
            cs_status.has_lang('de')

    def test_external_codeset(self):
        ts = terminology.TerminologyService()

        ids = terminology.OpenEHRCodeSetIdentifiers

        for cid in [ids.CODE_SET_ID_CHARACTER_SETS,
            ids.CODE_SET_ID_COMPRESSION_ALGORITHMS,
            ids.CODE_SET_ID_COUNTRIES,
            ids.CODE_SET_ID_INTEGRITY_CHECK_ALGORITHMS,
            ids.CODE_SET_ID_LANGUAGES,
            ids.CODE_SET_ID_MEDIA_TYPES,
            ids.CODE_SET_ID_NORMAL_STATUSES]:

            c = ts.code_set_for_id(cid)
            self.assertNotEqual(c, None)

        cs_countries = ts.code_set_for_id(ids.CODE_SET_ID_COUNTRIES)

        ac = cs_countries.all_codes()
        self.assertEqual(len(ac), 246)
        self.assertTrue(cs_countries.has_code(ac[0]))

        self.assertFalse(cs_countries.has_code(
            terminology.CodePhrase(identification.TerminologyID('ISO_639-1'), 'de')))
        self.assertTrue(cs_countries.has_code(
            terminology.CodePhrase(identification.TerminologyID('ISO_3166-1'), 'DE')))

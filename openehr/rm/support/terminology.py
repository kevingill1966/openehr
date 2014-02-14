#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os
from xml.etree.cElementTree import ElementTree as ET
from inspect import getmembers
from abc import ABCMeta, abstractmethod
from openehr.rm.support.identification import TerminologyID

OPENEHR_TERMINOLOGY_FILEPATH = os.path.join(os.path.dirname(__file__),"terminology.xml")

#----------------------------------------------------------------------------------------
#  INJECTION
#  Append objects to this dictionary providing your codeset accessors
#  Codeset name is used as the dictionary key.
#  The id attribute of the object is the codeset id.
AVAILABLE_CODE_SET={}
AVAILABLE_TERMINOLOGY={}

def register_codeset(name, accessor):
    if not isinstance(accessor, CodeSetAccess):
        raise ValueError("Accessor does not implement CodeSetAccess interface.")
    if name is None or type(name) != str or name.strip() == '':
        raise ValueError('The value is not valid Code Set identifier.')
    name = name.strip()
    AVAILABLE_CODE_SET[name] = accessor

def register_terminology(name, accessor):
    if not isinstance(accessor, TerminologyAccess):
        raise ValueError("Accessor does not implement TerminologyAccess interface.")
    if name is None or type(name) != str or name.strip() == '':
        raise ValueError('The value is not valid Terminology identifier. [%s]' % name)
    name = name.strip()
    AVAILABLE_TERMINOLOGY[name] = accessor

class CodeSetAccess(metaclass=ABCMeta):
    """
        baseclass for objects providing proxy access to a codeset.
        TODO: what to do about invariants
    """
    @abstractmethod
    def id(self):
        """External identity of this code set."""

    @abstractmethod
    def all_codes(self):
        """ Return all codes known in the code set.  """

    @abstractmethod
    def has_lang(self, a_lang):
        """ True if code set knows about 'a_lang'.  """

    @abstractmethod
    def has_code(self, a_code):
        """ True if code set knows about 'a_code'.  """

class TerminologyAccess(metaclass=ABCMeta):
    """
        baseclass for objects providing proxy access to a terminology.
        TODO: what to do about invariants
    """
    @abstractmethod
    def id(self):
        """Identification of this Terminology."""

    @abstractmethod
    def all_codes(self):
        """ Return all codes known in the terminology.  """

    @abstractmethod
    def codes_for_group_id(self, group_id):
        """ Return all codes under grouper 'group_id' from this terminology.  """

    @abstractmethod
    def has_code_for_group_id(self, group_id,a_code):
        """ True if 'a_code' is known in group 'group_id' in the openEHR terminology.  """

    @abstractmethod
    def codes_for_group_name(self, name, lang):
        """ Return all codes under grouper whose name in 'lang' is 'name' from this terminology.  """

    @abstractmethod
    def rubric_for_code(self, code,lang):
        "rubric of given code and language or None if not found"

#----------------------------------------------------------------------------------------

class OpenEHRCodeSetIdentifiers(object):


    CODE_SET_ID_CHARACTER_SETS=u'character sets'
    CODE_SET_ID_COMPRESSION_ALGORITHMS=u'compression algorithms'
    CODE_SET_ID_COUNTRIES=u'countries'
    CODE_SET_ID_INTEGRITY_CHECK_ALGORITHMS=u'integrity check algorithms'
    CODE_SET_ID_LANGUAGES=u'languages'
    CODE_SET_ID_MEDIA_TYPES=u'media types'
    CODE_SET_ID_NORMAL_STATUSES=u'normal statuses'


    def valid_code_set_id(self, an_id):
        u"""
        Boolean Validity function to test if an identifier is in
        the tuple defined by class OpenehrCodeSetIdentifiers.
        """
        code_sets = ( member_value for member_name,member_value in getmembers(self) if member_name.startswith(u'CODE_SET_ID_'))
        return an_id in code_sets


class OpenEHRTerminologyGroupIdentifiers(object):


    TERMINOLOGY_ID=u'openehr'
    GROUP_ID_AUDIT_CHANGE_TYPE=u'audit change type'
    GROUP_ID_ATTESTATION_REASON=u'attestation reason'
    GROUP_ID_COMPOSITION_CATEGORY=u'composition category'
    GROUP_ID_EVENT_MATH_FUNCTION=u'event math function'
    GROUP_ID_ISM_STATES=u'instruction states'
    GROUP_ID_ISM_TRANSITIONS=u'instruction transitions'
    GROUP_ID_NULL_FLAVOURS=u'null flavours'
    GROUP_ID_MEASURABLE_PROPERTIES=u'property'
    GROUP_ID_PARTICIPATION_FUNCTION=u'participation function'
    GROUP_ID_PARTICIPATION_MODE=u'participation mode'
    GROUP_ID_RELATED_PARTY_RELATIONSHIP=u'related party relationship'
    GROUP_ID_SETTING=u'setting'
    GROUP_ID_TERM_MAPPING_PURPOSE=u'term mapping purpose'
    GROUP_ID_VERSION_LIFECYCLE_STATE=u'version lifecycle state'


    def valid_terminology_group_id(self, an_id):
        groups_id = ( member_value for member_name,member_value in getmembers(self) if member_name.startswith('GROUP_ID_'))
        return an_id in groups_id


class CodeSetServiceMixIn(OpenEHRCodeSetIdentifiers):
    """
        Defines an object providing proxy access to codeset services. Published
        as TerminologyService.

        Codesets are injected into the AVAILABLE_CODE_SETS dictionary via run-time
        implementation.
    """

    def code_set(self, name):
        codeset_access = None
        if name is not None and name != '':
            external_name = name if not self.valid_code_set_id(name) else self.openehr_code_sets()[name]
            codeset_access = AVAILABLE_CODE_SETS.get(external_name, None)
        if codeset_access is None:
            raise ValueError('Code Set not found by the identifier specified. [%s]' % name)
        return codeset_access

    def code_set_for_id(self, id_):
        """
            Return an interface to the code_set identified internally in openEHR by id.
        """
        if id_ is not None and self.valid_code_set_id(id_):
            external_name = self.openehr_code_sets()[id_]
            codeset_access = AVAILABLE_CODE_SETS.get(external_name, None)
            if codeset_access is None:
                raise ValueError('Code Set not found by the identifier specified. [%s]' % id_)
            return codeset_access
        else:
            raise ValueError('The value is not valid code' \
                        ' set internal openEHR identifier.')

    def has_code_set(self, name):
        if name is not None and name != '':
            external_name = name if not self.valid_code_set_id(name) else self.openehr_code_sets()[name]
            return external_name in AVAILABLE_CODE_SETS
        raise ValueError('The value is not valid Code Set identifier.')

    def openehr_code_sets(self):
        return {
                self.CODE_SET_ID_LANGUAGES:'ISO_639-1',
                self.CODE_SET_ID_COUNTRIES:'ISO_3611-1',
                self.CODE_SET_ID_CHARACTER_SETS:'IANA_character-sets',
                self.CODE_SET_ID_COMPRESSION_ALGORITHMS:'openehr_compression_algorithms',
                self.CODE_SET_ID_INTEGRITY_CHECK_ALGORITHMS: 'openehr_integrity_check_algorithms',
                self.CODE_SET_ID_MEDIA_TYPES : 'IANA_media-types',
                self.CODE_SET_ID_NORMAL_STATUSES : 'openehr_normal_statuses',
                }

    def code_set_identifiers(self):
        return [ codesetaccess_obj.id() for codeset_access_obj in  AVAILABLE_CODE_SETS.values() ]

class TerminologyServiceMixIn(OpenEHRTerminologyGroupIdentifiers):
    """
        Defines an object providing proxy access to a terminology service.
        Published as TerminologyService.

        Terminology are injected into the AVAILABLE_TERMINOLOGY dictionary via run-time
        implementation.

        The allowed terminologies are defined in the terminology.xml file in this directory.
        These may not be implemented.
    """
    _vsab_terminology_identifiers = []

    def terminology(self, name):
        if name is not None and self.has_terminology(name):
            return AVAILABLE_TERMINOLOGY.get(name)
        else: raise ValueError("The name is not a valid Terminology identifier.")

    def has_terminology(self,name):
        is_a_term_id = name in self.terminology_identifiers()
        is_a_valid_name = name == self.TERMINOLOGY_ID or name == 'centc251'
        if name is not None and name != '' and (is_a_valid_name or is_a_term_id):
            return name in AVAILABLE_TERMINOLOGY
        else: raise ValueError("The name is not a valid terminology identifier.")

    def terminology_identifiers(self):
        return self._vsab_terminology_identifiers

    @classmethod
    def _bootstrap_terminologyservice(cls, root):
        """
            The XML file terminology.xml contains a set of concepts and terms which may be
            loaded as per terminology.pdf.

            Concept - defines a term
            Grouper - defines a terminolgoy
            GroupedConcept - links a terminolgy to a term 


           Example
              <Grouper id="13" ConceptID="248" />
              <PrimaryRubric Id="248" Language="en" />
              <Concept Language="en" ConceptID="248" Rubric="Audit change type" />
              <GroupedConcept GrouperID="13" ChildID="250" />
              <GroupedConcept GrouperID="13" ChildID="251" />
              <GroupedConcept GrouperID="13" ChildID="252" />
              <GroupedConcept GrouperID="13" ChildID="253" />
              <Concept Language="en" ConceptID="250" Rubric="amendment" />
              <Concept Language="en" ConceptID="251" Rubric="modification" />
              <Concept Language="en" ConceptID="252" Rubric="synthesis" />
              <Concept Language="en" ConceptID="253" Rubric="unknown" />

        """
        class OpenEHRTerminologyAccess(TerminologyAccess):
            """
                Accessor for the internal terminology 'openehr'.
            """
            _id = TerminologyID('openehr')
            _codes = None # CodePhrase objects
            _groupers = None
            _group_names = None
            _concepts = None

            def __init__(self, concepts, groupers):
                """
                    We are passed in a dict of concepts and groupers.
                """
                self._concepts = concepts

                self._codes = [CodePhrase(self._id, conceptid) for conceptid in concepts.keys()]
                self._groupers = {}
                self._group_names = {}
                for groupid, grouper in groupers.items():
                    self._groupers[groupid] = [CodePhrase(self._id, cid) for cid in grouper['conceptids']]
                    c = concepts[grouper['ConceptID']]
                    for lang in c.keys():
                        if lang not in self._group_names:
                            self._group_names[lang] = {}
                        self._group_names[lang][c[lang]['Rubric'].lower()] = groupid, c[lang]['Rubric']

            def id(self):
                return self._id

            def all_codes(self):
                return self._codes

            def codes_for_group_id(self, group_id):
                return self._groupers[group_id]

            def has_code_for_group_id(self, group_id, a_code):
                if group_id in self._groupers:
                    return a_code in self._groupers[group_id]
                return False

            def codes_for_group_name(self, name, lang):
                if lang in self._group_names:
                    group_id = self._group_names[lang].get(name.lower())[0]
                    if group_id is not None:
                        return self.codes_for_group_id(group_id)
                return None

            def rubric_for_code(self, code, lang):
                "rubric of given code and language or null if not found"
                concept = self._concepts.get(code)
                if concept and lang in concept:
                    return concept[lang].get('Rubric')
                return None

        conceptlist = [dict(d.items()) for d in root.findall('{http://openehr.org/Terminology.xsd}Concept')]
        concepts = {}
        for c in conceptlist:
            cid = c['ConceptID']
            if cid not in concepts: concepts[cid] = {}
            concepts[cid][c['Language']] = c
        groupers = [dict(d.items()) for d in root.findall('{http://openehr.org/Terminology.xsd}Grouper')]
        groupers = dict([(d['id'], d) for d in groupers])
        for g in groupers.values():
            g['conceptids'] = []
            
        for g in [dict(g.items()) for g in root.findall('{http://openehr.org/Terminology.xsd}GroupedConcept')]:
            try:
                grouper = groupers[g['GrouperID']] 
            except:
                print('Error cannot find grouper %s' % g)
                continue
            try:
                concept = concepts[g['ChildID']]
            except:
                print('Error cannot find concept %s' % g)
                continue
            grouper['conceptids'].append(g['ChildID'])
            
        openehr_terminology = OpenEHRTerminologyAccess(concepts, groupers)
        register_terminology('openehr', openehr_terminology)

        # Terminology identifiers - really this might be a codeset
        cls._vsab_terminology_identifiers = [t.get('VSAB')
                for t in root.findall('{http://openehr.org/Terminology.xsd}TerminologyIdentifiers')
                if t.get('VSAB')]

class CodePhrase:
    """
        This is a rm.datatype - I am concerned about the cross package dependencies.
    """
    terminologyid, codestring = None, None
    def __init__(self, terminologyid, codestring):
        self.terminologyid, self.codestring = terminologyid, codestring

class TerminologyService(TerminologyServiceMixIn, CodeSetServiceMixIn):
    @classmethod
    def bootstrap(cls):
        """
            The XML file terminology.xml contains a set of concepts and terms which may be
            loaded as per terminology.pdf.

            The file also contains code sets as follows.
              <Language code="af" Description="Afrikaans" />
        """
        class OpenEHRCodeSetAccess(CodeSetAccess):
            """
            """
            _id = None
            _base_lang = None
            _codes = None
            _translations = None

            def id(self):
                return self._id

            def all_codes(self):
                return self._codes

            @abstractmethod
            def has_lang(self, a_lang):
                """ True if code set knows about 'a_lang'.  """

            @abstractmethod
            def has_code(self, a_code):
                """ True if code set knows about 'a_code'.  """


        with open(OPENEHR_TERMINOLOGY_FILEPATH) as terminology_file:
            root = ET().parse(terminology_file)
            cls._bootstrap_terminologyservice(root)

# For now load this here: maybe should be taken out so it can be stopped
TerminologyService.bootstrap()
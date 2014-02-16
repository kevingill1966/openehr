# -*- coding: UTF-8 -*-

from openehr.rm.datatypes.basic import DataValue
from openehr.rm.support.terminology import TerminologyService
from openehr.rm.support.identification import TerminologyID


# TODO: mututal dependency between basic package and this
#       basic  provides DavaValue but uses DvCodedText


# Implementation is in TerminologyService by spec publishes it from this package
from openehr.rm.support.terminology import CodePhrase

class DvText(DataValue):
    """
    A text item, which may contain any amount of legal characters arranged as e.g.
    words, sentences etc (i.e. one DV_TEXT may be more than one word). Visual for-
    matting and hyperlinks may be included.
    A DV_TEXT can be "coded" by adding mappings to it.
    Fragments of text, whether coded or not are used on their own as values, or to
    make up larger tracts of text which may be marked up in some way, eventually
    going to make up paragraphs.

    """
    _value = _mappings = _formatting = _hyperlink = _language = _encoding = None

    @property
    def value(self):
        return self._value

    @property
    def mappings(self):
        return self._mappings

    @property
    def formatting (self):
        return self._formatting

    @property
    def hyperlink (self):
        return self._hyperlink

    @property
    def language(self):
        return self._language

    @property
    def encoding(self):
        return self._encoding

    @value.setter
    def value(self, value):
        if value is None or len(value.strip()) == 0:
            raise AttributeError('value attribute must not be None or empty')
        if '\n' in value or '\r' in value:
            raise AttributeError('carriage return and line feed characters not allowed in value attribute')
        self._value = value

    @mappings.setter
    def mappings(self, value):
        if value is not None and len(value) == 0:
            raise AttributeError('mappings must not be empty')
        self._mappings = value

    @formatting.setter
    def formatting(self, value):
        if value is not None and (not isinstance(value, str) or len(value.strip()) == 0):
            raise AttributeError('formatting must not be empty')
        self._formatting = value

    @hyperlink.setter
    def hyperlink(self, value):
        self._hyperlink = value

    @language.setter
    def language (self, value):
        self._language = value

    @encoding.setter
    def encoding(self, value):
        self._encoding = value


    def __init__(self, value, mappings=None, formatting=None, hyperlink=None, language=None, encoding=None, terminology_service=None):

        self.value=value
        self.mappings=mappings
        self.formatting = formatting
        self.hyperlink = hyperlink

        self.language = language
        self.encoding = encoding

        #TODO we need to remove this consistence when we finish the terminology_service
        if terminology_service is not None:
            CODE_SET_ID_LANGUAGES = TerminologyService.CODE_SET_ID_LANGUAGES
            code_set = terminology_service.code_set_for_id(CODE_SET_ID_LANGUAGES)
            if language is not None and not code_set.has_code(language):
                raise AttributeError('language must be in the language code set of the terminology service')

            CODE_SET_ID_CHARACTER_SETS = TerminologyService.CODE_SET_ID_CHARACTER_SETS
            code_set = terminology_service.code_set_for_id(CODE_SET_ID_CHARACTER_SETS)
            if encoding is not None and not code_set.has_code(encoding):
                raise AttributeError('encoding must be in the character code set of the terminology service')

    def __eq__(self, obj):
        if obj is self:
            return True
        if isinstance(obj, DvText):
            return obj.value ==  self.value and obj.encoding == self.encoding and obj.language == self.language
        return False

    def __hash__(self):
        result = 17
        result += 31 * result + hash(self.value)
        result += 31 * result + hash(self.encoding)
        result += 31 * result + hash(self.language)
        return result

    def __str__(self):
        return self.value

    def __repr__(self):
        return 'DvText(value: %s, mapping: %s, formatting: %s, hyperlink: %s, language: %s, encoding: %s)' % (self.value, self.mappings, self.formatting, self.hyperlink, self.language, self.encoding)

class DvCodedText(DvText):
    """
    A text item whose value must be the rubric from a controlled terminology, the
    key (i.e. the 'code') of which is the defining_code attribute. In other words: a
    DV_CODED_TEXT is a combination of a CODE_PHRASE (effectively a code) and
    the rubric of that term, from a terminology service, in the language in which the
    data was authored.

    Since DV_CODED_TEXT is a subtype of DV_TEXT, it can be used in place of it,
    effectively allowing the type DV_TEXT to mean "a text item, which may option-
    ally be coded".

    If the intention is to represent a term code attached in some way to a fragment of
    plain text, DV_CODED_TEXT should not be used; instead use a DV_TEXT and a
    TERM_MAPPING to a CODE_PHRASE.

    """
    _defining_code = None

    @property
    def defining_code(self):
        return self._defining_code

    @defining_code.setter
    def defining_code(self, value):
        if not isinstance(value, CodePhrase):
            raise AttributeError('defining_code  must not be of type CodePhrase [%s]' % value)
        self._defining_code = value

    def __init__(self,definingCode,value,mappings=None,formatting=None,hyperlink=None,language=None,encoding=None):
        self.definingCode=definingCode
        DvText.__init__(self,value,mappings,formatting,hyperlink,language,encoding)
 
class TermMapping(DataValue):
    """
    Represents a coded term mapped to a DV_TEXT, and the relative match of the tar-
    get term with respect to the mapped item. Plain or coded text items may appear in
    the EHR for which one or mappings in alternative terminologies are required.
    Mappings are only used to enable computer processing, so they can only be
    instances of DV_CODED_TEXT.

    Used for adding classification terms (e.g. adding ICD classifiers to SNOMED
    descriptive terms), or mapping into equivalents in other terminologies (e.g.
    across nursing vocabularies).

    """
    _target = _match = _purpose = None

    @property
    def target(self):
        return self._target
    @property
    def match(self):
        return self._match
    @property
    def purpose(self):
        return self._purpose

    @target.setter
    def target(self, value):
        if not isinstance(value, CodePhrase):
            raise AttributeError('target must be of type CodePrhase [%s]' % value)
        self._target = value

    @match.setter
    def match(self, value):
        if not isinstance(value, str) or len(value) != 1:
            raise AttributeError('match must be 1 character long [%s]' % value)
        if not self.is_valid_match_code(value):
            raise AttributeError("Invalid value for match [%s]" % value)
        self._match = value

    @purpose.setter
    def purpose(self, value):
        if value is not None and not isinstance(value, DvCodedText):
            raise AttributeError('purpose must be of type DvCodedText [%s]' % value)
        self._purpose = value

    def __init__(self, target, match, purpose, terminologyService=None):
        self.target = target
        self.match = match
        if purpose is not None:
            openehr_terminology = terminologyService.terminology(TerminologyService.TERMINOLOGY_ID)
            if not openehr_terminology.has_code_for_group_id(TerminologyService.GROUP_ID_TERM_MAPPING_PURPOSE, purpose.definingCode):
                raise AttributeError('Terminology service must have the purpose defining code')
        self.purpose = purpose

    def narrower(self):
        return self.match == '<'

    def equivalent(self):
        return self.match == '='

    def broader(self):
        return self.match == '>'

    def unknown(self):
        return self.match == '?'

    def is_valid_match_code(self, match):
        return match in ['<','>','=','?']


class DvParagraph(DataValue):
    """
    A logical composite text value consisting of a series of DV_TEXTs, i.e. plain text
    (optionally coded) potentially with simple formatting, to form a larger tract of
    prose, which may be interpreted for display purposes as a paragraph.
    DV_PARAGRAPH is the standard way for constructing longer text items in summa-
    ries, reports and so on.

    """
    _items = None

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        if not isinstance(value, list):
            raise AttributeError('items must be of type list [%s]' % value)
        for item in value:
            if not isinstance(value, DvText):
                raise AttributeError('items contents must be of type DvText [%s]' % value)
        self._items = value

    def __init__(self,items):
        self.items = items


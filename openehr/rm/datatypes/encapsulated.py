
from openehr.rm.datatypes.basic import DataValue
from openehr.rm.datatypes.uri import DvURI
from openehr.rm.datatypes.text import CodePhrase

class DvEncapsulated(DataValue):
    """Abstract class defining the common meta-data of all types of encapsulated data."""
    _charset = _language = _size = None

    @property
    def charset(self):
        return self._charset

    @property
    def language(self):
        return self._language

    @property
    def size(self):
        return self._size

    @charset.setter
    def charset(self, value):
        if value is not None and not isinstance(value, CodePhrase):
            raise AttributeError('charset attribute must be a CodePhrase')
        self._charset = value

    @language.setter
    def language(self, value):
        if value is not None and not isinstance(value, CodePhrase):
            raise AttributeError('language attribute must be a CodePhrase')
        self._language = value

    @size.setter
    def size(self, value):
        if type(value) != int:
            raise AttributeError('size attribute must be an integer')
        self._size = value


    def __init__(self, size, charset=None, language=None):
        self.charset = charset
        self.language = language
        self.size = size

    def as_string(self):
        return ""


class DvMultimedia(DvEncapsulated):
    """
    A specialisation of DvEncapsulated for audiovisual and biosignal types. Includes further
    metadata relating to multimedia types which are not applicable to other subtypes of DvEncapsulated.
    """
    _alternate_text = _media_type = _compression_algorithm  = _integrity_check = \
            _integrity_check_algorithm = _thumbnail = _uri = _data = None

    @property
    def alternate_text(self):
        return self._alternate_text

    @property
    def media_type(self):
        return self._media_type

    @property
    def compression_algorithm(self):
        return self._compression_algorithm

    @property
    def integrity_check(self):
        return self._integrity_check

    @property
    def integrity_check_algorithm(self):
        return self._integrity_check_algorithm

    @property
    def thumbnail(self):
        return self._thumbnail

    @property
    def uri(self):
        return self._uri

    @property
    def data(self):
        return self._data

    @alternate_text.setter
    def alternate_text(self, value):
        if value is not None and type(value) != str:
            raise AttributeError('alternate_text attribute must be a String')
        self._alternate_text = value

    @media_type.setter
    def media_type(self, value):
        if value is not None and not isinstance(value, CodePhrase):
            raise AttributeError('media_type attribute must be a CodePhrase')
        self._media_type = value

    @compression_algorithm.setter
    def compression_algorithm(self, value):
        if value is not None and not isinstance(value, CodePhrase):
            raise AttributeError('compression_algorithm attribute must be a CodePhrase')
        self._compression_algorithm = value

    @integrity_check.setter
    def integrity_check(self, value):
        if value is not None and type(value) != bytes:
            raise AttributeError('integrity_check attribute must be a byte string')
        self._integrity_check = value

    @integrity_check_algorithm.setter
    def integrity_check_algorithm(self, value):
        if value is not None and not isinstance(value, CodePhrase):
            raise AttributeError('integrity_check_algorithm attribute must be a CodePhrase')
        self._integrity_check_algorithm = value

    @thumbnail.setter
    def thumbnail(self, value):
        if value is not None and not isinstance(value, DvMultimedia):
            raise AttributeError('thumbnail attribute must be a DvMultiMedia')
        self._thumbnail = value

    @uri.setter
    def uri(self, value):
        if value is not None and not isinstance(value, DvURI):
            raise AttributeError('uri attribute must be a URI')
        self._uri = value

    @data.setter
    def data(self, value):
        if value is not None and  type(value) != bytes:
            raise AttributeError('data attribute must be a byte string')
        self._data = value

    def __init__(self, charset=None, language=None, alternate_text=None, media_type=None, compression_algorithm=None,
            integrity_check=None, integrity_check_algorithm=None, thumbnail=None, uri=None, data=None):
        self.alternate_text = alternate_text
        self.media_type = media_type
        self.compression_algorithm  = compression_algorithm
        self.integrity_check = integrity_check
        self.integrity_check_algorithm = integrity_check_algorithm
        self.thumbnail = thumbnail
        self.uri = uri
        self.data = data
        super(DvMultimedia, self).__init__(len(data), charset, language)

    def is_external(self):
        return isinstance(self.uri, DvURI)

    def is_inline(self):
        return self.data is not None and len(self.data) > 0

    def is_compressed(self):
        return isinstance(self.compression_algorithm, CodePhrase)

    def has_integrity_check(self):
        return isinstance(self.integrity_check_algorithm, CodePhrase)


class DvParsable(DvEncapsulated):
    _value = _formalism = None

    @property
    def value(self):
        return self._value

    @property
    def formalism(self):
        return self._formalism

    @value.setter
    def value(self, value):
        if value is not None and type(value) != str:
            raise AttributeError('value attribute must be a String')
        self._value = value

    @formalism.setter
    def formalism(self, value):
        if value is not None and type(value) != str:
            raise AttributeError('formalism attribute must be a String')
        self._formalism = value


    def __init__(self, value=None, formalism=None, charset=None, language=None):
        self.value = value
        self.formalism = formalism
        super(DvParsable, self).__init__(len(value), charset, language)

    def as_string(self):
        return self.value

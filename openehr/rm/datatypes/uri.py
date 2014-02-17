# -*- coding: UTF-8 -*-
import re
from urllib.parse import urlparse

from openehr.rm.datatypes.basic import DataValue

re_uri = r"[a-zA-z0-9+.-]+:" # scheme
re_uri += r"\S*$" # non space (should be pickier)
re_uri = re.compile(re_uri).match

class DvURI(DataValue):
    _uri_parsed = _value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, DvURI):
            value = value.value
        if value is None or type(value) != str or len(value.strip()) == 0:
            raise AttributeError('value attribute must not be None or empty')
        if '\n' in value or '\r' in value:
            raise AttributeError('carriage return and line feed characters not allowed in value attribute')
        if not re_uri(value):
            raise AttributeError('invalid uri [%s]' % value)
        self._value = value
        self._uri_parsed = urlparse(value)


    def __init__(self, value):
        self.value = value

    def scheme(self):
        return self._uri_parsed.scheme

    def path(self):
        """
            Not happy with this - seems to lose diffefence between relative and absolute paths.
            What should be done with parameters
        """
        rv = []
        if self._uri_parsed.netloc:
            rv.append('/' + self._uri_parsed.netloc)
        if self._uri_parsed.path:
            rv.append( self._uri_parsed.path)
        return ''.join(rv)

    def fragments_id(self):
        return self._uri_parsed.fragment

    def query(self):
        return self._uri_parsed.query

    def __eq__(self, other):
        if isinstance(other, DvURI):
            return self.value == other.value
        return False

    def __repr__(self):
        return 'DvURI(%s)' % self._value

class DvEHRURI(DvURI):
    """
    A DvEHRURI is a DvURI which has the scheme name ehr.

    TODO: how to call baseclass getter/setter
    """
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, DvURI):
            value = value.value
        if value is None or type(value) != str or len(value.strip()) == 0:
            raise AttributeError('value attribute must not be None or empty')
        if '\n' in value or '\r' in value:
            raise AttributeError('carriage return and line feed characters not allowed in value attribute')
        if not re_uri(value):
            raise AttributeError('invalid uri [%s]' % value)
        self._value = value
        self._uri_parsed = urlparse(value)

        if not self.scheme_is_ehr():
            raise AttributeError('Invalid scheme [%s], must be ehr' % self.scheme())

    def scheme_is_ehr(self):
        """ Never going to be false due to validator """
        return self.scheme() == 'ehr'

    def __repr__(self):
        return 'DvEHRURI(%s)' % self._value


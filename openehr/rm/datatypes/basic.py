# -*- coding: UTF-8 -*-
"""
	Copyright to be determined - copied from OSHIP

	Reference: datatypes_im.pdf Chapter 4 - Basic Package
"""

from abc import ABCMeta, abstractmethod



class DataValue(metaclass=ABCMeta):
    """
    Abstract class.
    Serves as a common ancestor of all data value types in openEHR models.

    These types are intended to be very rigid, so it is enforcing run-time
    type checking.
    """
    def __setattr__(self, name, value):
        """
            Generally, you cannot set values on the subclasses of DataValue.
            The subclasses provide explicit mechanisms to do so. They must
            bypass this logic by having a value with that name on the class.
        """
        if not hasattr(self, name):
            raise AttributeError('Unknown attribute [%s] for type %s' % (name, self.__class__))
        object.__setattr__(self, name, value)

    def _validate_invariant(self):
        """
            Specification defines a set of invariants. These are validated
            by executing this method.

            Should raise ValueError() or return
        """
    def __repr__(self):
        return 'DataValue(%s)' % (self.__class__)

    @abstractmethod
    def __init__(self):
        pass


class DvBoolean(DataValue):
    """
    Items which are truly boolean data, such as true/false answers.
    For such data, it is important to devise the meanings (usually questions in subjec-
    tive data) carefully, so that the only allowed results are in fact true or false.
    The DV_BOOLEAN class should not be used as a replacement for naively modelled
    enumerated types such as male/female etc. Such values should be coded, and in
    any case the enumeration often has more than two values.

    TODO: Boolean type allows NULL values - how to do this?
    """
    _value = None
    TRUE = FALSE = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value not in [True, False] and not isinstance(value, DvBoolean):
            raise AttributeError('Invalid value for DvBoolean: %s' % value)
        if isinstance(value, DvBoolean):
            self._value = value.value
        else:
            self._value = value

    def __init__(self, value):
        self.value = value

    def _validate_invariant(self):
        pass

    def __repr__(self):
        return 'DvBoolean(%s)' % (self.value)

    def __eq__(self, other):
        if isinstance(other, DvBoolean):
            return self.value == other.value
        if other == True:
            return self._value == True
        elif other == False:
            return self._value == False
        return False

DvBoolean.TRUE = DvBoolean(True)
DvBoolean.FALSE = DvBoolean(False)


class DvIdentifier(DataValue):
    """
    Type for representing identifiers of real-world entities. Typical identifiers include
    drivers licence number, social security number, vertans affairs number, prescrip-
    tion id, order id, and so on.
    DV_IDENTIFIER is used to represent any identifier of a real thing, issued by
    some authority or agency.
    DV_IDENTIFIER is not used to express identifiers generated by the infrastruc-
    ture to refer to information items; the types OBJECT_ID and OBJECT_REF and
    subtypes are defined for this purpose.
    """
    _issuer = _assigner = _id = _type = None

    @property
    def issuer(self):
        return self._issuer

    @property
    def assigner(self):
        return self._assigner

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @issuer.setter
    def issuer(self, value):
        if (value != None and not isinstance(value, str)) or (value != None and len(value) == 0):
            raise AttributeError('Invalid value for String: %s' % value)
        self._issuer = value

    @assigner.setter
    def assigner(self, value):
        if (value != None and not isinstance(value, str)) or (value != None and len(value) == 0):
            raise AttributeError('Invalid value for String: %s' % value)
        self._assigner = value

    @id.setter
    def id(self, value):
        if (value != None and not isinstance(value, str)) or (value != None and len(value) == 0):
            raise AttributeError('Invalid value for String: %s' % value)
        self._id = value

    @type.setter
    def type(self, value):
        if (value != None and not isinstance(value, str)) or (value != None and len(value) == 0):
            raise AttributeError('Invalid value for String: %s' % value)
        self._type = value

    def __init__(self, issuer, assigner=None, id=None, type=None):
        """
            Construct from a DvIdentifier or 4 strings
        """
        if isinstance(issuer, DvIdentifier):
            self.issuer = issuer.issuer
            self.assigner = issuer.assigner
            self.id = issuer.id
            self.type = issuer.type
        else:
            self.issuer = issuer
            self.assigner = assigner
            self.id = id
            self.type = type

    def __repr__(self):
        return 'DvIdentitifier(%s, %s, %s, %s)' % (self.issuer, self.assigner, self.id, self.type)

    def __eq__(self, other):
        if isinstance(other, DvIdentifier):
            return (
                    self.issuer == other.issuer and
                    self.assigner == other.assigner and
                    self.id == other.id and
                    self.type == other.type)
        return False



class DvState(DataValue):
    """
    For representing state values which obey a defined state machine, such as a vari-
    able representing the states of an instruction or care process.
    """
    _value = _is_terminal = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        #if not isinstance(value, DvCodedText):
        #    raise AttributeError('Invalid value for DvCodedText: %s' % value)
        self._value = value

    @property
    def is_terminal(self):
        return self._is_terminal

    @value.setter
    def is_terminal(self, value):
        if value not in [True, False]:
            raise AttributeError('Invalid value for Boolean: %s' % value)
        self._is_terminal = value

    def __init__(self, value, is_terminal):
        self.value = value
        self.is_terminal = is_terminal

    def __repr__(self):
        return 'DvState(%s, is_terminal=%s)' % (self.value, self.is_terminal)

    def __eq__(self, other):
        if isinstance(other, DvState):
            return self.value == other.value and self.is_terminal == other.is_terminal
        return False


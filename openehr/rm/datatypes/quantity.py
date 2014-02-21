# -*- coding: UTF-8 -*-


import copy

from openehr.rm.datatypes.basic import DataValue
from openehr.rm.datatypes.text import DvCodedText, DvText, CodePhrase
from openehr.rm.support import Interval


class NonParametrizedValue(Exception):
    pass


class DvOrdered(DataValue):

    _normal_range = _other_reference_ranges = _normal_status = None

    @property
    def normal_range(self):
        return self._normal_range

    @property
    def other_reference_ranges(self):
        return self._other_reference_ranges

    @property
    def normal_status(self):
        return self._normal_status

    @normal_range.setter
    def normal_range(self, value):
        if value is not None and not isinstance(value, DvInterval):
            raise AttributeError('normal_range attribute must be a DvInterval')
        if value is not None and value.lower.__class__ != self.__class__:
            raise NonParametrizedValue(("The normal_range attribute must"
                    " include a lower attribute from the same type as this object."))
        self._normal_range = value

    @other_reference_ranges.setter
    def other_reference_ranges(self, value):
        if value is not None:
            if type(value) != list:
                raise AttributeError('other_reference_ranges attribute must be a list')
            for ref_range in value:
                if not isinstance(ref_range, DvOrdered):
                    raise AttributeError('other_reference_ranges must contain DvOrdered types only')
                if ref_range.range.lower.__class__ != self.__class__:
                    raise NonParametrizedValue(("The items from the"
                            "other_reference_ranges must include a lower"
                            "attribute from  the same type as this object."))

        self._other_reference_ranges = value

    @normal_status.setter
    def normal_status(self, value):
        if value is not None and not isinstance(value, CodePhrase):
            raise AttributeError('normal_status attribute must be a CodePhrase')
        self._normal_status = value

    def __init__(self, normal_range=None, other_reference_ranges=None, normal_status=None):
        self.normal_range = normal_range
        self.other_reference_ranges = other_reference_ranges
        self.normal_status = normal_status

    def is_simple(self):
        if self.normal_range is None and self.other_reference_ranges is None:
            return True
        return False

    def is_normal(self):
        has_range = self.normal_range is not None
        has_status = self.normal_status is not None
        if has_range:
            if self.normal_range.has(self):
                return True
        elif has_status:
            if self.normal_status.code_string == "N":
                return True
        else: raise TypeError("The object doesn't have any normal range.")
        return False

    def is_strictly_comparable_to(self, other):
        class_name = self.__class__.__name__
        raise NotImplementedError("The class %s must implement this method." %(class_name))

    def __lt__(self,other):
        class_name = self.__class__.__name__
        raise NotImplementedError("The class %s must implement the < operator." %(class_name))


class DvOrdinal(DvOrdered):
    _value = _symbol = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value is not None and type(value) != int:
            raise AttributeError('value attribute must be an Integer')
        self._value = value

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        if value is not None and not isinstance(value, DvCodedText):
            raise AttributeError('symbol attribute must be a DvCodedText')
        self._symbol = value

    def __init__(self, value, symbol, normal_range=None, other_reference_ranges=None, normal_status=None):
        self.value = value
        self.symbol = symbol
        super(DvOrdinal, self).__init__(normal_range=normal_range, other_reference_ranges=other_reference_ranges, normal_status=normal_status)

    def limits(self):
        """
            Seems to find the 'limits' range in the other_reference_ranges list
        """
        meaning = DvText('limits')
        if self.other_reference_ranges:
            for r in self.other_reference_ranges:
                if r.meaning == meaning:
                    return r
        return None

    def is_strictly_comparable_to(self, other):
        """
            TODO: see java code
        """
        return self.symbol == other.symbol

    def __lt__(self, other):
        if self.is_strictly_comparable_to(other):
            return self.value < other.value
        return False

    def __eq__(self, other):
        if self.is_strictly_comparable_to(other):
            return self.value == other.value
        return False


class DvQuantified(DvOrdered):
    _magnitude = _accuracy = _magnitude_status = None
    VALID_STATUS = ['=', '>', '<', '<=', '>=', '~']


    @property
    def magnitude(self):
        return self._magnitude

    @magnitude.setter
    def magnitude(self, value):
        if value is not None and type(value) not in [int, float]:
            raise AttributeError('magnitude attribute must be an Integer or float')
        self._magnitude = value

    @property
    def accuracy(self):
        return self._accuracy

    @accuracy.setter
    def accuracy(self, value):
        self._accuracy = value

    @property
    def accuracy_unknown(self):
        return self._accuracy == None

    @property
    def magnitude_status(self):
        return self._magnitude_status

    @magnitude_status.setter
    def magnitude_status(self, value):
        if value is not None and value not in self.VALID_STATUS:
            raise AttributeError('magnitude_status attribute must be one of: %s' % self.VALID_STATUS)
        self._magnitude_status = value


    def __init__(self, magnitude, accuracy=None, normal_range=None, other_reference_ranges=None, normal_status=None, magnitude_status=None):
        self.magnitude = magnitude
        self.accuracy = accuracy
        self.magnitude_status = magnitude_status
        super(DvQuantified, self).__init__(normal_range=normal_range, other_reference_ranges=other_reference_ranges, normal_status=normal_status)

    def valid_magnitude_status(self,val):
        return val in self.VALID_STATUS


class DvAbsoluteQuantity(DvQuantified):
    """
        TODO: There is maths add/subtract/diff to be worked out here
    """
    pass


class DvAmount(DvQuantified):
    UNKNOWN_ACCURACY_VALUE = -1.0

    _accuracy_is_percent = None

    @property
    def accuracy_is_percent(self):
        return self._accuracy_is_percent

    @accuracy_is_percent.setter
    def accuracy_is_percent(self, value):
        if value is not None and type(value) != bool:
            raise AttributeError('value attribute must be a Boolean')
        self._accuracy_is_percent = value

    def __init__(self, magnitude, accuracy=UNKNOWN_ACCURACY_VALUE, accuracy_is_percent=False, magnitude_status="=", normal_range=None, other_reference_ranges=None, normal_status=None):
        super(DvAmount, self).__init__(magnitude=magnitude, accuracy=accuracy, normal_range=normal_range, other_reference_ranges=other_reference_ranges, normal_status=normal_status, magnitude_status=magnitude_status)
        self.accuracy_is_percent = accuracy_is_percent

    def valid_percentage(self,val):
        return val >= 0.0 and val <= 100.0

    @property
    def accuracy_unknown(self):
        return self.accuracy == self.UNKNOWN_ACCURACY_VALUE

    def __add__(self,other):
        assert self.is_strictly_comparable_to(other)
        klass = type(self)
        return self._do_arithmetic_expression(other,klass,"+")

    def __sub__(self,other):
        assert self.is_strictly_comparable_to(other)
        klass = type(self)
        return self._do_arithmetic_expression(other,klass,"-")

    def __neg__(self):
        negated_copy = copy.copy(self)
        negated_copy.magnitude = -self.magnitude
        return negated_copy

    def __lt__(self,other):
        assert self.is_strictly_comparable_to(other)
        this_magnitude = self.magnitude() if callable(self.magnitude) else self.magnitude
        other_magnitude = other.magnitude() if callable(other.magnitude) else other.magnitude
        return this_magnitude < other_magnitude

    def _do_arithmetic_expression(self,other,klass,operator):
        has_ac_unknown = self.accuracy_unknown
        other_has_ac_unknown = other.accuracy_unknown
        other_has_percent = other.accuracy_is_percent
        has_percent = self.accuracy_is_percent
        new_obj_data = {}
        if has_ac_unknown or other_has_ac_unknown:
             new_obj_data['accuracy'] = self.UNKNOWN_ACCURACY_VALUE
        elif has_percent^other_has_percent:
            chosen_accuracy = max(self.accuracy,other.accuracy)
            new_obj_data['accuracy_is_percent'] = False
            if chosen_accuracy == other.accuracy and other.accuracy_is_percent:
                new_obj_data['accuracy_is_percent'] = True
            elif chosen_accuracy == self.accuracy and self.accuracy_is_percent:
                new_obj_data['accuracy_is_percent'] = True
            new_obj_data['accuracy'] = chosen_accuracy
        else:
            if has_percent and other_has_percent:
                new_obj_data['accuracy_is_percent'] = True
            new_accuracy = eval("float(self.accuracy"+operator+"other.accuracy)")
            new_obj_data['accuracy'] = new_accuracy 
        this_magnitude = self.magnitude() if callable(self.magnitude) else self.magnitude
        other_magnitude = other.magnitude() if callable(other.magnitude) else other.magnitude
        new_obj_data['magnitude'] = eval("this_magnitude" + operator + "other_magnitude")
        obj = klass(**new_obj_data)
        return obj


class DvCount(DvAmount):

    @property
    def magnitude(self):
        return self._magnitude

    @magnitude.setter
    def magnitude(self, value):
        if value is not None and type(value) not in [int]:
            raise AttributeError('magnitude attribute must be an Integer')
        self._magnitude = value

    def __lt__(self, val):
        if not isinstance(val, DvCount):
            raise TypeError("Argument type must be DvCount")
        return self.magnitude < val.magnitude

    def __gt__(self, val):
        if not isinstance(val, DvCount):
            raise TypeError("Argument type must be DvCount")
        return self.magnitude > val.magnitude

    def __eq__(self, val):
        if not isinstance(val, DvCount):
            raise TypeError("Argument type must be DvCount")
        return self.magnitude == val.magnitude

    def __add__(self, val):
        if not isinstance(val, DvCount):
            raise TypeError("Argument type must be DvCount")
        else:
            return DvCount(magnitude = self.magnitude + val.magnitude,
                    accuracy=self.accuracy, accuracy_is_percent=self.accuracy_is_percent, magnitude_status=self.magnitude_status,
                    normal_status=self.normal_status, normal_range=self.normal_range, other_reference_ranges=self.other_reference_ranges)

    def __sub__(self, val):
        if not isinstance(val, DvCount):
            raise TypeError("Argument type must be DvCount")
        else:
            return DvCount(magnitude = self.magnitude - val.magnitude, 
                    accuracy=self.accuracy, accuracy_is_percent=self.accuracy_is_percent, magnitude_status=self.magnitude_status,
                    normal_status=self.normal_status, normal_range=self.normal_range, other_reference_ranges=self.other_reference_ranges)

    def __neg__(self):
        return DvCount(magnitude = -self.magnitude, 
                    accuracy=self.accuracy, accuracy_is_percent=self.accuracy_is_percent, magnitude_status=self.magnitude_status,
                    normal_status=self.normal_status, normal_range=self.normal_range, other_reference_ranges=self.other_reference_ranges)


class DvInterval(DataValue, Interval):
    def __init__(self, lower, upper, lower_included=None, upper_included=None):
        Interval.__init__(self, lower, upper, lower_included, upper_included)


class ProportionKind(object):
    pk_ratio = 0
    pk_unitary = 1
    pk_percent = 2
    pk_fraction = 3
    pk_integer_fraction = 4

    def valid_proportion_kind(self, n):
        return n in (self.pkRatio, self.pkUnitary, self.pkPercent, self.pkFraction, self.pkIntegerFraction)

class DvProportion(DvAmount, ProportionKind):
    _precision = _type = _numerator = _denominator = None

    @property
    def numerator(self):
        return self._numerator

    @numerator.setter
    def numerator(self, value):
        if type(value) not in [int, float]:
            raise AttributeError('numerator attribute must be an Integer or Float')
        self._numerator = value

    @property
    def denominator(self):
        return self._denominator

    @denominator.setter
    def denominator(self, value):
        if type(value) not in [int, float]:
            raise AttributeError('denominator attribute must be an Integer or Float')
        self._denominator = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if type(value) not in [int]:
            raise AttributeError('type attribute must be an Integer ')
        self._type = value

    @property
    def precision(self):
        return self._precision

    @precision.setter
    def precision(self, value):
        if value is not None and type(value) not in [int]:
            raise AttributeError('precision attribute must be an Integer ')
        self._precision = value


    def __init__(self, numerator, denominator, type=None, precision=None, accuracy=None, accuracy_is_percent=None, magnitude=None, normal_range=None, other_reference_ranges=None, normal_status=None):
        self.numerator = numerator
        self.denominator = denominator
        self.type = type
        self.precision = precision
        self._validate_attributes()

        DvAmount.__init__(self, accuracy=accuracy, accuracy_is_percent=accuracy_is_percent, magnitude=magnitude, normal_range=normal_range, other_reference_ranges=other_reference_ranges, normal_status=normal_status)

    def _validate_attributes(self):
        _type = self.type
        numerator = self.numerator
        denominator = self.denominator
        precision = self.precision

        # Constraints
        if _type == ProportionKind.pk_unitary:
            if denominator != 1:
                raise AttributeError("denominator for unitary proportion must be 1")

        elif _type == ProportionKind.pk_percent:
            if denominator != 100:
                raise AttributeError("denominator for unitary proportion must be 100")

        elif _type == ProportionKind.pk_fraction or _type == ProportionKind.pk_integer_fraction:
            if not (type(numerator) == int and type(denominator) == int):
                raise AttributeError("both numberator and denominator must be integral for " +
                    "fraction or integer fraction proportion")
        
        if type(numerator) == int and type(denominator) == int and (precision != None and precision != 0):
            raise AttributeError( "precision must be 0 if both numerator and denominator are integral")

        if not (type(numerator) == int and type(denominator) == int) and (precision == None or precision == 0):
            raise AttributeError("zero precision for non-integral numerator or denominator")


    def is_integral(self):
        return isinstance(self.numerator, int) and isinstance(self.denominator, int)

    def magnitude(self):
        """
            TODO: may conflict with the magnitude attribute
        """
        return self.numerator / self.denominator


class DvQuantity(DvAmount):
    _units = _precision = None

    @property
    def precision(self):
        return self._precision

    @precision.setter
    def precision(self, value):
        if value is not None and type(value) not in [int]:
            raise AttributeError('precision attribute must be an Integer ')
        if value is not None and value < 0:
            raise AttributeError('precision must be positive or zero ')
        self._precision = value

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        if value is not None and type(value) not in [str]:
            raise AttributeError('units attribute must be a String ')
        self._units = value

    @property
    def magnitude(self):
        return self._magnitude

    @magnitude.setter
    def magnitude(self, value):
        if type(value) == int:
            value = float(value)
        if value is not None and type(value) not in [float]:
            raise AttributeError('magnitude attribute must be a Float')
        self._magnitude = value

    def __init__(self, magnitude, units=None, precision=None, accuracy=None, accuracy_is_percent=None, normal_range=None, other_reference_ranges=None, normal_status=None):
        self.units = units
        self.precision=precision
        super(DvQuantity,  self).__init__(accuracy=accuracy, accuracy_is_percent=accuracy_is_percent, magnitude=magnitude,
                normal_range=normal_range, other_reference_ranges=other_reference_ranges, normal_status=normal_status)

    def is_integral(self):
        """True if precision = 0; quantity represents an integral number."""
        return self.precision == 0


    def is_strictly_comparable_to(self, other):
        if (isinstance(other, self.__class__)):
            return self.units==other.units and self.magnitude==other.magnitude

    def __str__(self):
        if self.units:
            return '%.*f,%s' % (self.precision or 0, self.magnitude, self.units)
        else:
            return '%.*f' % (self.precision or 0, self.magnitude)

    def __eq__(self, other):
        if self.is_strictly_comparable_to(other):
            return self.magnitude == other.magnitude and self.units == other.units and self.precision == other.precision
        return False

class ReferenceRange(DvOrdered):
    _range = _meaning = None
    NORMAL = 'normal'

    @property
    def meaning(self):
        return self._meaning

    @meaning.setter
    def meaning(self, value):
        if not isinstance(value, DvText):
            raise AttributeError('meaning attribute must be a DvText')
        self._meaning = value

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, value):
        if not isinstance(value, DvInterval):
            raise AttributeError('range attribute must be a DvInterval')
        self._range = value

    def __init__(self, meaning, range, normal_range=None, other_reference_ranges=None, normal_status=None):
        self.meaning = meaning
        self.range = range

        super(ReferenceRange, self).__init__(normal_range=normal_range, other_reference_ranges=other_reference_ranges, normal_status=normal_status)

    def is_in_range(self,val):
        return self.range.has(val)


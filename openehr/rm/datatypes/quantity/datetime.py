# -*- coding: UTF-8 -*-


import re
import math
import copy
from mx.DateTime import DateTimeFrom, TimeFrom, DateFrom
from openehr.rm.datatypes.quantity import (DvAbsoluteQuantity,
                                             DvAmount, DvQuantified)
from openehr.rm.support import TimeDefinitions

# TODO: drop mx and some of this code from isodate package.
#       for now install mx package and get the tests running.


ISO8601_REGEX = re.compile(r'^P([0-9]+Y)?([0-9]+M)?([0-9]+W)?([0-9]+D)?(T([0-9]+H)?([0-9]+M)?([0-9]+([,.][0-9]+)?S)?)?$')


class DvDuration(DvAmount,TimeDefinitions):
    _value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value is not None and type(value) != str:
            raise AttributeError('value attribute must be an String')
        self._value = value

    sign = '+'

    def __init__(self,value_or_magnitude='',accuracy=DvAmount.UNKNOWN_ACCURACY_VALUE,
                      magnitude_status=None,accuracy_is_percent=False,normal_range=None,
                      other_reference_ranges=None,normal_status=None,**kwargs):
        if kwargs.has_key('magnitude'):
            value_or_magnitude = kwargs['magnitude']
        if isinstance(value_or_magnitude,basestring):
            self.value = unicode(value_or_magnitude)
        elif isinstance(value_or_magnitude,float) or isinstance(value_or_magnitude,int):
            if value_or_magnitude < 0:
                self.sign = '-'
                value_or_magnitude = math.fabs(value_or_magnitude)
            self.value = unicode(self._convert_to_str(value_or_magnitude))
        else:
            raise AttributeError("Invalid value")
        if not self.valid_ISO8601_duration(self.value):
            raise AttributeError("Invalid value")
        self.accuracy_is_percent = accuracy_is_percent
        self.accuracy = accuracy
        if magnitude_status is None or self.valid_magnitude_status(magnitude_status):
            self.magnitude_status = magnitude_status
        else:
            raise ValueError("Magnitude status must be '=', '>', '<', '<=', '>=', '~' or None")
        super(DvQuantified,self).__init__(normal_range, other_reference_ranges, normal_status)

    def magnitude(self):
        return self.to_seconds()

    def _convert_to_str(self,seconds):
        """Convert seconds using the ISO format: 
           P[nnY][nnM][nnW][nnD][T[nnH][nnM][nnS]] .
        """
        if seconds == 0:
            return 'PT0S'
        date_time_parts = {'Y':0,
                           'M':0,
                           'W':0,
                           'D':0,
                           'h':0,
                           'm':0,
                           's':0}
        date_time_order = ('Y',
                           'M',
                           'W',
                           'D',
                           'h',
                           'm',
                           's',)
        remaining_seconds = seconds
        date_string = 'P'
        time_string = ''
        date_list = []
        time_list = []

        for symbol in date_time_order:
            converter_multiplier = self._get_converted_divisor(symbol)
            if remaining_seconds < converter_multiplier:
                continue
            elif remaining_seconds == converter_multiplier:
                date_time_parts[symbol] = 1
                remaining_seconds = 0
                break
            else:
                date_time_int, remaining_seconds = self._convert_duration(remaining_seconds,converter_multiplier)
                date_time_parts[symbol] = date_time_int
        date_time_parts['s'] += remaining_seconds

        for symbol in date_time_order:
            if date_time_parts[symbol] == 0:
                continue
            if symbol.isupper():
                date_list.append(str(date_time_parts[symbol])+symbol)
            elif symbol.islower():
                time_list.append(str(date_time_parts[symbol])+symbol.upper())
        date_string += ''.join(date_list)
        if len(time_list) != 0:
            time_string = ''.join(time_list)
            time_string = 'T'+time_string

        return unicode(date_string+time_string)

    def to_seconds(self):
        years_in_seconds = self.years()*self._get_converted_divisor('Y')
        months_in_seconds = self.months()*self._get_converted_divisor('M')
        weeks_in_seconds = self.weeks()*self._get_converted_divisor('W')
        days_in_seconds = self.days()*self._get_converted_divisor('D')
        hours_in_seconds = self.hours()*self._get_converted_divisor('h')
        minutes_in_seconds = self.minutes()*self._get_converted_divisor('m')

        date_seconds = (years_in_seconds + months_in_seconds + weeks_in_seconds + days_in_seconds)
        time_seconds = (hours_in_seconds + minutes_in_seconds + self.seconds() + self.fractional_second())
        total_seconds = date_seconds + time_seconds
        if self.sign == '-':
            return -total_seconds
        return total_seconds


    def _get_converted_divisor(self,time_symbol):
        """
        Catch the corrected divisor to seconds unit,
        using the mapping unit symbol - multiplier.
        """
        min_to_sec = self.SECONDS_IN_MINUTES
        hour_to_sec = min_to_sec*self.SECONDS_IN_MINUTES
        day_to_sec = hour_to_sec*self.HOURS_IN_DAY
        week_to_sec = day_to_sec*self.DAYS_IN_WEEK
        month_to_sec = day_to_sec*self.NOMINAL_DAYS_IN_MONTH
        year_to_sec = day_to_sec*self.NOMINAL_DAYS_IN_YEAR
        duration_parts = {
                      's':1,
                      'm':min_to_sec,
                      'h':hour_to_sec,
                      'D':day_to_sec,
                      'W':week_to_sec,
                      'M':month_to_sec,
                      'Y':year_to_sec}

        return duration_parts[time_symbol]
  
    def _convert_duration(self,seconds,multiplier):
        """
        Do the math to compute the ISO string from each unit,
        passing the arguments the total seconds.
        It returns the remaing seconds and the unit quantity specified.
        Ex: 31556737.0 seconds(which represent 1 year and 1 seconds in seconds) 
            and 31556736.0 (year multiplier) returns (1,1.0) .
        """
        quantified_duration = math.trunc(seconds / multiplier)
        remaining_seconds = math.fmod(seconds , multiplier)
        return (quantified_duration,remaining_seconds)

    def years(self):
        return self._get_specific_date_time('Y')

    def months(self):
        return self._get_specific_date_time('M')

    def weeks(self):
        return self._get_specific_date_time('W')

    def days(self):
        return self._get_specific_date_time('D')

    def hours(self):
        return self._get_specific_date_time('H')

    def minutes(self):
        return self._get_specific_date_time('TM')

    def seconds(self):
        return self._get_specific_date_time('S')

    def fractional_second(self):
        return self._get_specific_date_time('FS')
   
    def _get_specific_date_time(self,symbol):
        """
        Catch the defined value on each date or time, based on
        mapping between the regex and the unit symbol.
        """
        specific_date_time = 0
        symbol_position_map = {'Y':1,
                               'M':2,
                               'W':3,
                               'D':4,
                               'H':6,
                               'TM':7,
                               'S':8,
                               'FS':8
                               }
        captured_match = ISO8601_REGEX.match(self.value)
        if captured_match is not None:
            verified_part = captured_match.group(symbol_position_map[symbol])
            if verified_part is not None:
                verified_part = verified_part[:-1]
                if symbol == 'FS' or symbol == 'S':
                    decimal_sign = '.'
                    if self.is_decimal_sign_comma():
                        decimal_sign = ','
                    fractional_parts = verified_part.split(decimal_sign)
                    if symbol == 'FS':
                        if len(fractional_parts) == 2:
                            specific_date_time = '0.'+fractional_parts[1]
                        else: specific_date_time = '0.0'
                        specific_date_time = float(specific_date_time)
                    else:
                        specific_date_time = int(fractional_parts[0])
                else:
                    specific_date_time = int(verified_part)
        return specific_date_time
   
    def valid_ISO8601_duration(self,s):
        if self.value == '' or self.value == 'P' or self.value == 'PT': return False
        captured_match = ISO8601_REGEX.match(self.value)
        if captured_match is not None: return True
        return False

    def is_decimal_sign_comma(self):
        captured_match = ISO8601_REGEX.match(self.value)
        seconds_string = captured_match.group(9)
        if seconds_string is not None:
            return ',' in seconds_string
        return False

    def is_strictly_comparable_to(self, other):
        if isinstance(other, DvDuration):
            return True
        return False
 
    def __eq__(self,other):
        if self.is_strictly_comparable_to(other):
            same_magnitude = self.magnitude() == other.magnitude()
            same_accuracy_type = other.accuracy_is_percent == self.accuracy_is_percent
            same_accuracy = self.accuracy == other.accuracy
            if same_magnitude and same_accuracy and same_accuracy_type:
                return True
        return False

    def __neg__(self):
        new_obj = copy.copy(self)
        if new_obj.sign == '+':
            new_obj.sign = '-'
        else: new_obj.sign = '+'
        return new_obj

    def __str__(self):
        return self.value

    def __unicode__(self):
        return self.value


class DvTemporal(DvAbsoluteQuantity):
    """
    Abstract class. Specialised temporal variant of DV_ABSOLUTE_QUANTITY whose diff type is
    DV_DURATION.
    """

    def __init__(self,magnitude,accuracy,normalRange,otherReferenceRanges,normalStatus,magnitudeStatus=None):
        self.magnitude = magnitude
        DvAbsoluteQuantity.__init__(self,magnitude,accuracy,normalRange,otherReferenceRanges,normalStatus,magnitudeStatus)


class DvDate(DvTemporal):
    """
    Represents an absolute point in time, as measured on the Gregorian calendar, and
    specified only to the day. Semantics defined by ISO 8601.
    Used for recording dates in real world time. The partial form is used for
    approximate birth dates, dates of death, etc.
    """

    def __init__(self,value,magnitude,accuracy,normalRange,otherReferenceRanges,normalStatus):
        self.value = value
        dt1 = DateFrom(value)
        dt2 = DateFrom('0000-01-01')
        dtDiff = dt1 - dt2
        magnitude = dtDiff.days

        DvTemporal.__init__(self,magnitude,accuracy,normalRange,otherReferenceRanges,normalStatus)


    def diff(self,other):
        """
        Difference of two dates. 'other' must be a DvDate. Returns a DvDuration.
        """

        diffdays = self.magnitude - other.magnitude

        return DvDuration(diffdays)

    def valueValid(self):
        """validIso8601DateTime(value)"""

        return DateTimeFrom(self.value) is not None


class DvDateTime(DvTemporal):
    """
    Represents an absolute point in time, specified to the second. Semantics defined by ISO 8601.
    Used for recording a precise point in real world time, and for approximate time
    stamps, e.g. the origin of a HISTORY in an OBSERVATION which is only partially known.
    """

    def __init__(self,value,magnitude,accuracy,normalRange,otherReferenceRanges,normalStatus):
        self.value = value
        dt1 = DateTimeFrom(value)
        dt2 = DateTimeFrom('0000-01-01T00:00:00')
        dtDiff = dt1 - dt2
        magnitude = dtDiff.seconds

        DvTemporal.__init__(self,magnitude,accuracy,normalRange,otherReferenceRanges,normalStatus)

    def diff(self,other):
        """Difference of two date/times. Returns a DvDuration"""
        diffsecs = self.magnitude - other.magnitude

        return DvDuration(diffsecs)


    def valueValid(self):
        """validIso8601DateTime(value)"""

        return DateTimeFrom(self.value) is not None


class DvTime(DvTemporal):
    """
    Represents an absolute point in time from an origin usually interpreted as meaning the start
    of the current day, specified to the second. Semantics defined by ISO8601.

    Used for recording real world times, rather than scientifically measured fine
    amounts of time. The partial form is used for approximate times of events and
    substance administrations.
    """

    def __init__(self,value,magnitude,accuracy,normalRange,otherReferenceRanges,normalStatus):
        self.value=value
        dt1 = TimeFrom(value)
        dt2 = TimeFrom('00:00:00')
        dtDiff = dt1 - dt2
        magnitude = dtDiff.seconds
        DvTemporal.__init__(self,magnitude,accuracy,normalRange,otherReferenceRanges,normalStatus)

    def diff(self,other):
        """Difference of two times. Returns a DvDuration"""
        diffsecs = self.magnitude - other.magnitude

        return DvDuration(diffsecs)



    def valueValid(self):
        """validIso8601DateTime(value)"""

        return DateTimeFrom(self.value) is not None

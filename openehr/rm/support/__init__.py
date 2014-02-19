# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2007, Timothy W. Cook and Contributors. All rights reserved.
# Redistribution and use are governed by the MPL license.
#
# Use and/or redistribution of this file assumes you have read and accepted the
# terms of the license.
##############################################################################


"""
    This code is taken oship.

    Support Information Model Rev. 1.0.2
"""

__author__ = u'Timothy Cook <timothywayne.cook@gmail.com>'
__docformat__ = u'plaintext'
__contributors__ = (u'Fabricio Ferracioli <fabricioferracioli@gmail.com>',
    u'Sergio Miranda Freire <sergio@lampada.uerj.br>')


import calendar

class Smallest(object):
    """Represents the smallest value

      This type doesn't do much; it implements a pseudo-value that's smaller
      than everything but itself.
    """

    def __neg__(self):
        """Returns the largest value

            The opposite of negative infinity is infinity, the largest value.
        """
        return Largest()

    def __lt__(self, other):
        """Compares this with another object

            Always indicates that self is less than other, unless both are of
            type Smallest, in which case they are equal.
        """
        if other.__class__ == self.__class__:
            retval = False
        else:
            retval = True
        return retval

    def __gt__(self, other):
        return False

    def __str__(self):
        """Returns a printable representation of this value

          The string for the smallest number is -~, which means negative infinity.
        """
        return "-~"

    def __repr__(self):
        """Returns an evaluable representation of the object

            The representation of the smallest number is -Inf, which means
            negative infinity.
        """
        return "-Inf"

    def __hash__(self):
        "Returns a value that can be used for generating hashes"
        return 0x55555555


class Largest(object):
    """Class representing the universal largest value

        This type doesn't do much; it implements a pseudo-value that's larger
        than everything but itself.
    """

    def __neg__(self):
        """Returns the smallest universal value

        The opposite of infinity is negative infinity, the smallest value.
        """
        return Smallest()

    def __lt__(self, other):
        """Compares object with another object

        Always indicates that self is greater than other, unless both are of
        type Largest, in which case they are equal.

        """
        return False

    def __gt__(self, other):
        """Compares object with another object

        Always indicates that self is greater than other, unless both are of
        type Largest, in which case they are equal.

        """
        if other.__class__ == self.__class__:
            retval = False
        else:
            retval = True
        return retval


    def __str__(self):
        """Returns a string representation of the object

          The largest number is displayed as ~ (it sort of looks like infinity...)
          """
        return "~"

    def __repr__(self):
        """Returns an evaluable expression representing this object
        """
        return "Inf"

    def __hash__(self):
        "Returns a value that can be used for generating hashes"
        return -0x55555555


class Interval(object):

    lower = lower_unbounded = lower_included = upper = upper_unbounded = upper_included = None

    def __init__(self, lower=Smallest(), upper=Largest(),
                 lower_included=False, upper_included=False, **kw):

        """Initializes an interval

          Parameters ========== - lower: The lower bound of an interval
          (default Smallest()) - upper: The upper bound of an interval
          (default Largest()) - lower_included: Boolean telling if the
          lower value of interval are included (default True).  -
          upper_included: Boolean telling if the greater value of interval
          are included (default True)
        """
        if (lower is None or upper is None):
            raise ValueError('lower and upper must not be None')

        if (not isinstance(lower, Smallest) and not
            isinstance(upper, Largest)):
            if (type(lower) != type(upper)):
                raise TypeError('lower and upper must be of the same type')
        if (not callable(getattr(lower, '__lt__'))
            or not callable(getattr(upper, '__lt__'))):
            raise NotImplementedError('Classes are not comparable.'
                                      ' Implement __lt__ methods')

        if (lower > upper):
            raise ValueError('lower must be less than or equal to upper')

        if (lower_included and isinstance(lower, Smallest)):
            raise ValueError('lower_included implies lower greater than -Inf')

        if(upper_included and isinstance(upper, Largest)):
            raise ValueError('upper_included implies upper greater than Inf')

        self.lower = lower
        if (isinstance(lower, Smallest)):
            self.lower_unbounded = True
        else:
            self.lower_unbounded = False
        self.lower_included = lower_included

        self.upper = upper
        if (isinstance(upper, Largest)):
            self.upper_unbounded = True
        else:
            self.upper_unbounded = False
        self.upper_included = upper_included

    def __hash__(self):
        """
            Returns a hashed value of the object
            Intervals are to be considered immutable.  Thus, a 32-bit hash can
            be generated for them.
        """
        return hash((self.lower_unbounded, self.upper_unbounded, 
                     self.lower, self.upper, self.lower_included, self.upper_included))

    def __eq__(self, other):
        if isinstance(other, Interval):
            return hash(self) == hash(other)
        return False

    def __repr__(self):
        """
            Returns an evaluable expression that can reproduce the object
        """
        return "Interval(lower=%s, upper=%s, lower_unbounded=%s, upper_unbounded=%s, \
        lower_included=%s, upper_included=%s)" % (repr(self.lower), repr(self.upper), \
        repr(self.lower_unbounded),repr(self.upper_unbounded), repr(self.lower_included), \
        repr(self.upper_included))

    def has(self, value):
        """
            Returns if a value is inside the interval
        """

        if (value is None):
            raise ValueError('value must not be None')

        if (type(value) == type(self)):
            raise TypeError('value must be of the same type as self')

        #the value is between Smallest and Largest
        if (isinstance(self.lower, Smallest) and isinstance(self.upper, Largest)):
            return True
        #Smallest is the value of self.lower and upper is finite,
        #need to test the value of upper
        elif (isinstance(self.lower, Smallest)):
            if (value < self.upper):
                return True
            else:
                #test for the upper closed interval
                return self.upper_included and value == self.upper
        #Largest is the value of self.upper and lower is finite,
        #need to test the value of lower
        elif (isinstance(self.upper, Largest)):
            if (value > self.lower):
                return True
            else:
                #test for the lower closed interval
                return self.lower_included and value == self.lower
        else:
            #test for intervals that upper and lower values are finite
            if (value > self.lower and value < self.upper):
                return True
            else:
            #test for closed values
                if (self.lower_included and value == self.lower):
                    return True
                elif (self.upper_included and value == self.upper):
                    return True
                else:
                    return False


class TimeDefinitions(object):

    SECONDS_IN_MINUTES = 60;
    MINUTES_IN_HOUR = 60;
    HOURS_IN_DAY = 24;
    NOMINAL_DAYS_IN_MONTH = 30.42;
    MAX_DAYS_IN_MONTH = 31;
    DAYS_IN_YEAR = 365;
    DAYS_IN_LEAP_YEAR = 366;
    MAX_DAYS_IN_YEAR =  DAYS_IN_LEAP_YEAR;
    NOMINAL_DAYS_IN_YEAR = 365.24;
    DAYS_IN_WEEK = 7;
    MONTHS_IN_YEAR = 12;
    MIN_TIMEZONE_HOUR = 12;
    MAX_TIMEZONE_HOUR = 13;
    
    def valid_year(self,y):
        return y>= 0;

    def valid_month(self,m):
        return m>=1 and m<=self.MONTHS_IN_YEAR

    def valid_day(self,y,m,d):
        return d>= 1 and d in self.days_in_month(m,y)

    def days_in_month(self,m,y):
        try:
            days = calendar.monthrange(y,m)[1]
        except ValueError:
            days = 0
        return xrange(1,days+1)

    def valid_hour(self,h,m,s):
        return (h>=0 and h<self.HOURS_IN_DAY) or (h==self.HOURS_IN_DAY and m==0 and s==0)

    def valid_minute(self,m):
        return m>=0 and  m<self.MINUTES_IN_HOUR

    def valid_second(self,s):
        return s>=0 and s<self.SECONDS_IN_MINUTES

    def valid_fractional_second(self,fs):
        return fs>=0  and fs<1



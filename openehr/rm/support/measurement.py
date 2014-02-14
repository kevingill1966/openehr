# -*- coding: utf-8 -*-

"""
    Trivial implementation of the Measurement service defined in the spec.

    Don't see any services implemented in oship. Class does not seem to 
    be implemented in the java lib at all.
"""

#--------------------------------------------------------------
# Injection Approach
MEASUREMENT_INFO_SERVICES = []
def register_measurement_info_service(s):
    if s not in MEASUREMENT_INFO_SERVICES:
        MEASUREMENT_INFO_SERVICES.append(s)
#--------------------------------------------------------------

class MeasurementService(object):
    """Defines an object providing proxy access to a measurement
    information service."""

    def is_valid_units_string(self, units):
        """ True if the units string 'units' is a valid string
        according to the HL7 UCUM specification.  units is not None
        """
        if type(units) != str or not units.strip():
            raise AttributeError('Invalid value for units: %s' % units)

        for service in MEASUREMENT_INFO_SERVICES:
            if service.is_valid_units_string(units):
                return True
        return False


    def units_equivalent(self, units1, units2):
        """ True if two units strings correspond to the same measured property.
        """
        if type(units1) != str or not units1.strip():
            raise AttributeError('Invalid value for units1: %s' % units1)
        if type(units2) != str or not units2.strip():
            raise AttributeError('Invalid value for units2: %s' % units2)

        for service in MEASUREMENT_INFO_SERVICES:
            units1_valid = service.is_valid_units_string(units1)
            units2_valid = service.is_valid_units_string(units2)
            if units1_valid and units2_valid:
                return service.units_equivalent(units1, units2)
        return False


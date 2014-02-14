"""
From oship...

    Measurement Service
    ===================

    A measurement service should provide ways to verify if
    a unit is valid and if two units use the same measurement unit.
    To make this concept clear: Gb(Gigabit) and Mb(Megabit) use 
    the same property unit. The Measurement Service provides useful 
    functions to other modules of the OpenEHR Reference Model, mainly 
    to the `oship.openehr.rm.datatypes.quantity` module.
    The MeasurementService class provide access to operations that enable
    to do that. It can validate units which can come from a 
    variety of sources, such as:

    * CEN ENV 12435, Medical Informatics - Expression of results of measurements
    in health sciences .

    * the Unified Code for Units of Measure (UCUM), developed by Gunther Schadow 
    and Clement J. McDonald of The Regenstrief Institute .

    So, Every time a unit is verified, a MeasurementService object acts like a proxy
    to these measurement sources, verifying which one can answer if units are
    valid units::
"""


from openehr.rm.support.measurement import MeasurementService, \
    register_measurement_info_service

import unittest

class TestVersionID(unittest.TestCase):
    def test_invalid_service(self):
        ms = MeasurementService()
        self.assertFalse(ms.is_valid_units_string('miles'))

    def test_simple_service(self):
        ms = MeasurementService()

        class SimpleService:
            def __init__(self):
                self.units = ['milimeter', 'kilometer', 'centimeter', "meter"]
            def is_valid_units_string(self, unit):
                if unit in self.units:
                    return True
                return False
            def units_equivalent(self, units1, units2):
                if self.is_valid_units_string(units1) and self.is_valid_units_string(units2):
                    return True
                return False

        register_measurement_info_service(SimpleService())

        self.assertTrue(ms.is_valid_units_string("meter"))
        self.assertFalse(ms.is_valid_units_string("pascal"))

        self.assertTrue(ms.units_equivalent("meter", "centimeter"))
        self.assertTrue(ms.units_equivalent("kilometer", "milimeter"))
        self.assertFalse(ms.units_equivalent("kilometer", "kilogram"))

        #   Using this mechanism you can add different measurement sources, covering
        #   different types of measurement units::

        class AnotherService(SimpleService):
            def __init__(self):
                self.units = ['gram', 'kilogram']
        register_measurement_info_service(AnotherService())

        self.assertTrue(ms.is_valid_units_string("gram"))
        self.assertTrue(ms.is_valid_units_string("milimeter"))
        self.assertTrue(ms.units_equivalent("kilogram", "gram"))
        self.assertTrue(ms.units_equivalent("kilometer", "centimeter"))
        self.assertFalse(ms.units_equivalent("kilogram", "meter"))


        # Using this mechanism, new measurement sources can be included. It's important
        # to notice that two sources don't have relation between them. For example, let's
        # consider two sources: a source has the only the 'gram' unit and a second source 
        # have just the 'kilogram' unit provided by themselves. In the real world, they are 
        # considered equivalent but this cannot be considered true here because they are
        # related to different sources. In other hand, they are considered valid 
        # because each source validate those units::

        class LastService(SimpleService):
            def __init__(self):
                self.units = ['decimeter', 'centigram', 'kilogram']
        register_measurement_info_service(LastService())

        self.assertTrue(ms.is_valid_units_string("decimeter"))
        self.assertTrue(ms.is_valid_units_string("centigram"))
        self.assertFalse(ms.units_equivalent('meter', 'decimeter'))
        self.assertTrue(ms.units_equivalent('centigram', 'kilogram'))
        self.assertTrue(ms.units_equivalent('kilogram', 'gram'))
        self.assertFalse(ms.units_equivalent('centigram', 'gram'))

    def test_invalid_parameters(self):
        ms = MeasurementService()
        with self.assertRaises(AttributeError):
            ms.is_valid_units_string(4)
        with self.assertRaises(AttributeError):
            ms.is_valid_units_string(None)
        with self.assertRaises(AttributeError):
            ms.is_valid_units_string('')
        with self.assertRaises(AttributeError):
            ms.units_equivalent('centigram', '')
        with self.assertRaises(AttributeError):
            ms.units_equivalent(None, 'centigram')

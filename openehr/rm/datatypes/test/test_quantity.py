
import unittest

from openehr.rm.datatypes.quantity import DvOrdered, DvOrdinal, \
    DvQuantified, DvAbsoluteQuantity, DvAmount, DvCount, \
    DvInterval, DvProportion, DvQuantity, ReferenceRange, NonParametrizedValue
from openehr.rm.datatypes.text import CodePhrase, DvCodedText
from openehr.rm.support.identification import TerminologyID
from openehr.rm.datatypes.text import DvText, TermMapping
from openehr.rm.datatypes.uri import DvURI

class TestDvOrdered(unittest.TestCase):
    def test_oship_doctest(self):
        """
            oship doctest 

            Describing ordered values with DvOrdered
            ========================================

            Objects which that follow DvOrdered type must define the concept of ordered
            values, which includes ordinals as well as true quantities.  It defines the
            functions ‘<’ and is_strictly_comparable_to, the latter of which must evaluate
            to True for instances being compared with the ‘<’ function, or used as limits in
            the `DvInterval` class.  The DvOrdered class is a abstract class. So, is
            mandatory create a concrete class, and stub classes to exercise it's behaviors::
        """

        class SimpleOrderedNumber(DvOrdered):
            value = None
            def __init__(self,value,**kwargs):
                super(SimpleOrderedNumber,self).__init__(**kwargs)
                self.value = value

        class StubText(DvText):
            def __init__(self,value):
                self.value = value
                self.mappings = None
                self.encoding = None
                self.formatting = None
                self.language = None
        class StubInterval(DvInterval):
            def __init__(self,lower,upper):
                self.lower = lower
                self.upper = upper
            def has(self,item):
                if self.lower < item and item < self.upper:
                    return True
                else: return False

        class RefRange(ReferenceRange):
            def __init__(self,meaning,range):
                self.meaning = StubText(meaning)
                self.range = range
            def is_in_range(self):
                pass

        class DummyTerminologyID(object):
            pass

        class DummyCodePhrase(CodePhrase):
            def __init__(self,code_string):
                self.code_string = code_string
                self.terminologyId = DummyTerminologyID()
                
                
        """
            All DvOrdered object follows the DataValue interface. It means that it must
            have a value attribute.
        """

        diabetes_result = SimpleOrderedNumber(5)
        self.assertEqual(diabetes_result.value, 5)

        """
            The `DvOrdered` class provides a method called `is_simple` which defines if a
            DvOrdered object have reference ranges or not.  A reference range is a quantity
            range attached to a measured value, and usually used on laboratory result
            values. For example, a desirable total cholesterol is < 5.5 mmol/L. In fact, an
            expected and wel accepted value is between 2 and 5.5 mmol/L. This kind of reference
            range is defined on `normal_range` attribute.
            In other hand, progesterone and pituitary hormones have ranges which are
            different for different phases of the menstrual cycle and for menopause. This
            may result in 4 or 5 ranges given for one result. Only one will apply to any
            particular patient - but the exact phase of the cycle may be unknown - so the
            ranges may need to be associated with the value with no 'normal' range. These
            ranges can be defined using the `other_reference_ranges` attribute which is a
            collection of reference ranges.
            Following this principle, `is_simple` and `is_normal` methods work on these
            reference ranges, defining if a measurement range is associated or
            if the defined value is included in any expected range,respectively::
        """

        self.assertTrue(diabetes_result.is_simple())

        """
            If a object don't any have ranges, `is_normal` cannot verify if the value is in
            a range. So, an exception is raised if this scenario is true::
        """

        second_result = SimpleOrderedNumber(3)
        with self.assertRaises(TypeError):
            second_result.is_normal()

        """
            The `is_stricty_comparable_to` method is used to verify if two objects can be
            comparable. It can used by the `__lt__` method in order to define a sort order
            bewteen objects.
        """

        with self.assertRaises(NotImplementedError):
            second_result.is_strictly_comparable_to(diabetes_result)

        """
            The DvOrdered doesn't implement it. The same case applies to the < operator
            which is defined by `__lt__` method. It's used to define a simple sorted set of
            values on the same domain(e.g. a DvInterval).
        """

        with self.assertRaises(NotImplementedError):
            second_result < diabetes_result

        """
            The `normal_status` attribute is a `CodePhrase` object that allows define a symbol
            that is coded according to the openEHR terminology group "normal status", and
            takes values 'HHH' (critically high), 'HH' (abnormally high), 'H' (borderline
            high)', 'N' (normal), 'L' ... 'LLL'. In the quantity range domain, it is also is
            used to define laboratory results showing which level the value is.  To verify
            completely the ability of check if a value is normal, is mandatory both
            the interval limit(lower and upper atrtibutes) and the value itself have the <
            (`__lt__` method) operator implemented. So, let's create a more complete DvOrdered 
            that match all requirements::
        """


        class OrderedNumber(SimpleOrderedNumber):
            def is_strictly_comparable_to(self, other):
                class_name = other.__class__.__name__
                if class_name == "OrderedNumber":
                    return True
                else: return False
            def __lt__(self,other):
                if self.is_strictly_comparable_to(other):
                    return self.value < other.value
                else: TypeError("The object type doesn't match")

        diabetes_range = StubInterval(OrderedNumber(2),OrderedNumber(5.5))
        final_diabetes_result = OrderedNumber(4, normal_range=diabetes_range)
        self.assertTrue(final_diabetes_result.is_normal())

        final_diabetes_result = OrderedNumber(9, normal_range=diabetes_range)
        self.assertFalse(final_diabetes_result.is_normal())

        self.assertFalse(final_diabetes_result.is_simple())

        final_diabetes_result = OrderedNumber(7,normal_status=DummyCodePhrase(u"HHH"))
        self.assertFalse(final_diabetes_result.is_normal())

        final_diabetes_result = OrderedNumber(7,normal_status=DummyCodePhrase("N"))
        self.assertTrue(final_diabetes_result.is_normal())

        """
            If both `normal_status` and `normal_range` are found in a DvOrdered object, they
            must be valid to the value result be considered normal. If the value is not in
            the range, and the status is not normal (anything different from the
            symbol that represents normal, defined in the openehr terminology) the method
            `is_normal` will return False::
        """


        complete_diabetes_result = OrderedNumber(7, normal_range=diabetes_range,normal_status=DummyCodePhrase(u"N"))
        self.assertFalse(complete_diabetes_result.is_normal())

        complete_diabetes_result = OrderedNumber(3, normal_range=diabetes_range,normal_status=DummyCodePhrase(u"N"))
        self.assertTrue(complete_diabetes_result.is_normal())

        """
            The `normal_range` and `other_reference_ranges` attributes must follow the same
            type of the value related::
        """

        estrogen_ref_ranges = []
        prepubertal_estrogen_level = RefRange("Prepubertal",StubInterval(OrderedNumber(12),OrderedNumber(57)))
        estrogen_ref_ranges.append(prepubertal_estrogen_level)
        follicular_phase = RefRange("Folicular Phase", StubInterval(OrderedNumber(29),OrderedNumber(525)))
        estrogen_ref_ranges.append(follicular_phase)
        luteal_phase = RefRange("Luteal Phase",StubInterval(OrderedNumber(126),OrderedNumber(478)))
        estrogen_ref_ranges.append(luteal_phase)
        posmenupausal = RefRange("PosMenupausal",StubInterval(OrderedNumber(23),OrderedNumber(103)))
        estrogen_ref_ranges.append(posmenupausal)
        estrogen_result = OrderedNumber(100,other_reference_ranges=estrogen_ref_ranges,normal_status=DummyCodePhrase(u"LL"))

        self.assertFalse(estrogen_result.is_simple())
        self.assertFalse(estrogen_result.is_normal())

        """
            When a DvOrdered is created, every DvOrdered object composited in it must be checked
            if they are the same type::
        """

        diff_interval = StubInterval(SimpleOrderedNumber(12), SimpleOrderedNumber(200))
        with self.assertRaises(NonParametrizedValue):
            estrogen_result = OrderedNumber(30, normal_range=diff_interval)

        range_different_type = RefRange(u"weird range",diff_interval)
        other_estrogen_range = [range_different_type,follicular_phase]
        with self.assertRaises(NonParametrizedValue):
            other_estrogen_result = OrderedNumber(30,other_reference_ranges=other_estrogen_range,normal_status=DummyCodePhrase(u"L"))


        """
            DvOrdered Invariants
            --------------------

            The DvOrdered invariants are used a few restrictions that must be applied.

            The other_reference_ranges never must be a empty collection but it can be None::
        """

        # - equivalent? IDvOrdered.validateInvariants(diabetes_result)

        ordered_value_with_ranges = OrderedNumber(1,other_reference_ranges=[])
        #>>> IDvOrdered.validateInvariants(ordered_value_with_ranges)
        #Traceback (most recent call last):
        #...
        #Invalid: The other_reference_ranges cannot be empty.


        """
            The `is_simple` method must be consistent always::
        """

        not_simple_value = OrderedNumber(45)
        old_simple = DvOrdered.is_simple
        def new_simple(self):
            return False

        DvOrdered.is_simple = new_simple
        # IDvOrdered.validateInvariants(not_simple_value)
        # Traceback (most recent call last):
        # ...
        # Invalid: There is a inconsistency: the is_simple method cannot validate correctly.

        """
            If both `normal_range` and `normal_status` cannot be well defined at the same time::
        """
    
        DvOrdered.is_simple = old_simple
        simple_interval = StubInterval(OrderedNumber(2),OrderedNumber(6))
        weird_value = OrderedNumber(3,normal_range=simple_interval,normal_status=DummyCodePhrase(u"N"))
        # >>> IDvOrdered.validateInvariants(weird_value)
        # Traceback (most recent call last):
        # ...
        # Invalid: Both normal_status and normal_range are defined and validated correctly. Only one of them can be validated by the time.


    def testIsNormalWithoutNormalStatusAndNormalRange(self):
        count = DvCount(accuracy=0, accuracy_is_percent=False, magnitude=1)
        with self.assertRaises(TypeError):
            count.is_normal()

    def testIsNormalWithNormalStatus(self):
        normalStatus = CodePhrase("normal statuses", "N")
        count = DvCount(normal_status=normalStatus, accuracy=0, accuracy_is_percent=False, magnitude=1)       
        self.assertTrue(count.is_normal())

    def testIsNormalWithAbnormalStatus(self):
        normalStatus = CodePhrase("normal statuses", "L")
        count = DvCount(normal_status=normalStatus, accuracy=0, accuracy_is_percent=False, magnitude=1)
        self.assertFalse(count.is_normal())

    def testIsNormalWithNormalRange(self):
        normalRange = DvInterval(DvCount(0), DvCount(2))
        count = DvCount(normal_range=normalRange, accuracy=0, accuracy_is_percent=False, magnitude=1)
        self.assertTrue(count.is_normal());
    
    def testIsNormalWithNoneInclusiveNormalRange(self):
        normalRange = DvInterval(DvCount(2), DvCount(4))
        count = DvCount(normal_range=normalRange, accuracy=0, accuracy_is_percent=False, magnitude=1)       
        self.assertFalse(count.is_normal());
    
    def testIsNormalWithNormalStatusAndNormalRange(self):
        normalRange = DvInterval(DvCount(0), DvCount(2))
        normalStatus = CodePhrase("normal statuses", "N")
        count = DvCount(normal_range=normalRange, normal_status=normalStatus, accuracy=0,
                    accuracy_is_percent=False, magnitude=1)
        self.assertTrue(count.is_normal());
    

class TestDvOrdinal(unittest.TestCase):
    def test_constructor(self):
        tid = TerminologyID("SNOMED-CT(2003)")
        cp = CodePhrase(tid, "abc123")
        ct = DvCodedText(cp, "abc123")
        o = DvOrdinal(value=1, symbol=ct)
        self.assertEqual(type(o), DvOrdinal)

class SimpleDvQuantified(DvQuantified):
    pass

class TestDvQuantified(unittest.TestCase):

    def setUp(self):
        self.a_quantity = SimpleDvQuantified(2)
        self.valid_magnitude_status = ('=','>','<','<=','>=','~',)

    def test_commom_properties(self):
        self.assertTrue(self.a_quantity.normal_status is None)
        self.assertTrue(self.a_quantity.normal_range is None)
        self.assertTrue(self.a_quantity.other_reference_ranges is None)
        self.assertEqual(self.a_quantity.magnitude, 2)
        self.assertTrue(self.a_quantity.accuracy is None)
        self.assertTrue(self.a_quantity.magnitude_status is None)
        self.assertTrue(self.a_quantity.accuracy_unknown)

    def test_valid_magnitude_status_with_valid_values(self):
        for status in self.valid_magnitude_status:
           self.assertTrue(self.a_quantity.valid_magnitude_status(status))

    def test_valid_magnitude_status_with_invalid_values(self):
        self.assertFalse(self.a_quantity.valid_magnitude_status('a'))
        self.assertFalse(self.a_quantity.valid_magnitude_status(''))
        self.assertFalse(self.a_quantity.valid_magnitude_status(None))

    def test_constructor_with_invalid_magnitude_status(self):
        with self.assertRaises(AttributeError):
            SimpleDvQuantified(2,magnitude_status='a')
        with self.assertRaises(AttributeError):
            SimpleDvQuantified(3,magnitude_status='')

    def test_constructor_with_valid_magnitude_status(self):
        for status in self.valid_magnitude_status:
            another_quantity = SimpleDvQuantified(6,magnitude_status=status)
            self.assertEqual(status, another_quantity.magnitude_status)

    def test_constructor_with_a_None_magnitude_status(self):
        a_quantity = SimpleDvQuantified(78)
        self.assertEqual(None, a_quantity.magnitude_status)

    def test_magnitude_invariant(self):
        a_simple_quantity = SimpleDvQuantified(None)
        assert a_simple_quantity.magnitude is None
        # self.assertRaises(Invalid, IDvQuantified.validateInvariants, a_simple_quantity)

    def test_magnitude_status_invariant(self):
        a_simple_quantity = SimpleDvQuantified(42, "=")
        with self.assertRaises(AttributeError):
            a_simple_quantity.magnitude_status = "doh!"
        # self.assertRaises(Invalid, IDvQuantified.validateInvariants, a_simple_quantity)




class TestDvAbsoluteQuantity(unittest.TestCase):
        pass

class TestDvAmount(unittest.TestCase):
    def test_oship_doctest(self):
        """
        Defining quantity amounts with DvAmount
        =======================================

        An `DvAmount` class represents relative quantified 'amounts'.  The amount here
        means amounts about something, which allows defines either a physical property,
        such as a mass, or items in general(cigarettes, for example).  The arithmetic
        operators(+, - , * and /) and any other in the mathematical field act here as a
        true numbers. In case two relative quantities are evaluated using these
        operators and they have the same measured property, it should create other relative
        quantity of the same type. If was executed a subtraction as an arithmetic operation,
        the scenario happens in the same way : another object is created.
        The only mandatory attributes to create a `DvAmount` is the magnitude attribute,
        which is the number that corresponds how amount will be represented.  The
        optional attributes are the magnitude_status and accuracy following the
        `IDvQuantified` interface and normal_range, other_reference_ranges and
        normal_status attributes specified by `IDvOrdered` interface.  In order to
        exercise it's operations which are defined on the abstract class, concrete
        classes must be defined.  The DvAmount is a abstract class, which means that
        object cannot be a direct instance of it. All antecessors parameters
        and behaviors still valid::
        """

        class Amount(DvAmount):
            def is_strictly_comparable_to(self,other):
                if other.__class__ == self.__class__:
                    return True
                return False
            def __lt__(self,other):
                assert self.is_strictly_comparable_to(other)
                return self.magnitude < other.magnitude
        class AnotherAmount(DvAmount):
            pass

        box_quantity = Amount(7)
        self.assertEqual(box_quantity.normal_range, None)
        self.assertEqual(box_quantity.other_reference_ranges, None)
        self.assertEqual(box_quantity.normal_status, None)
        self.assertEqual(box_quantity.accuracy, -1.0)
        self.assertEqual(box_quantity.magnitude_status, u'=')
        self.assertEqual(box_quantity.magnitude, 7)
        with self.assertRaises(TypeError):
            box_quantity.is_normal()

        self.assertEqual(box_quantity.is_simple(), True)
        self.assertTrue(box_quantity.valid_magnitude_status(u"="))

        weird_amount = AnotherAmount(2)
        with self.assertRaises(NotImplementedError):
            weird_amount + box_quantity

        """
        The only mandatory methods that must be implemented to pass on all abstract
        restrictions are is_strictly_comparable_to, and __lt__ which is the < operator.
        The is_strictly_comparable_to is used by other methods to verify if two object
        can be compared correctly.
        The Amount class defined here for test purposes, have all requirements to a true
        `DvAmout` concrete class::
        """

        other_box_quantity = Amount(5)
        self.assertFalse(box_quantity < other_box_quantity)
        all_boxes = box_quantity + other_box_quantity
        self.assertFalse(all_boxes.magnitude< 12)
        self.assertTrue(all_boxes.magnitude< 13)
        negated_box_quantity= -all_boxes
        self.assertEqual(negated_box_quantity.magnitude, -12)

        """
        Setting accuracy in a DvAmount object
        -------------------------------------

        The *accuracy* of a value usually isn't included in a model for quantified
        values. In the realistic health domain, it's required for statistical purposes
        allowing make queries which the measurement error can be disambiguated from a
        true correlation. For practical purposes, a (in)accuracy corresponds to a range
        of possible values.  A value of 0 in either case indicates 100% accuracy, i.e.
        no error in measurement. The method unknown_accuracy verifies if the accuracy
        was measured::
        """

        main_room_brightlight = Amount(magnitude=200,accuracy=200.0)
        self.assertFalse(main_room_brightlight.accuracy_is_percent)
        wait_room_brightlight = Amount(magnitude=300,accuracy=150.0)
        sheets_of_paper = Amount(500)
        self.assertTrue(sheets_of_paper.accuracy_unknown)
        more_sheets_of_papers = Amount(70, accuracy=0.0)
        self.assertFalse(more_sheets_of_papers.accuracy_unknown)
        a_set_of_simple_chairs = Amount(magnitude=50,accuracy=80.0,accuracy_is_percent=True)
        self.assertFalse(a_set_of_simple_chairs.accuracy_unknown)
        a_set_of_elegant_chairs = Amount(70, accuracy=300.0)
        self.assertFalse(a_set_of_elegant_chairs.accuracy_is_percent)

        """
        Where accuracy is not recorded in a quantity, it is represented by a special
        value. In `DvAmount`, the `UNKNOWN_ACCURACY_VALUE` value is used for this
        purpose.  In addition, the class `DvAmount`, provides a attribute called
        accuracy_is_percent: A boolean to indicate if accuracy value is to be understood
        as a percentage, or an absolute value.

        When two compatible quantities are added or subtracted using the + or -
        operators (`DvAmount` descendants), the accuracy behaves in the following way:

        * if accuracies are present in both quantities, they are added in the result,
        for both addition and subtraction operations::
        """

        total_bright = main_room_brightlight + wait_room_brightlight
        self.assertEqual(total_bright.magnitude, 500)
        self.assertEqual(total_bright.accuracy, 350.0)
        
        turn_wait_room_lights_off = main_room_brightlight - wait_room_brightlight
        self.assertEqual(turn_wait_room_lights_off.magnitude, -100)
        self.assertEqual(turn_wait_room_lights_off.accuracy, 50.0)

        """
            if either or both quantities has an unknown accuracy, the accuracy of the
            result is also unknown::
        """

        total_sheets = sheets_of_paper + more_sheets_of_papers 
        self.assertEqual(total_sheets.magnitude, 570)
        self.assertTrue(total_sheets.accuracy_unknown)
        the_best_sheets = sheets_of_paper - more_sheets_of_papers
        self.assertEqual(the_best_sheets.magnitude, 430)
        self.assertTrue(the_best_sheets.accuracy_unknown)

        """
            if two `DvAmount` descendants are added or subtracted, and only one has
            accuracy_is_percent equals True, accuracy is expressed in the form used
            in the larger of the two quantities::
        """

        all_chairs = a_set_of_simple_chairs + a_set_of_elegant_chairs
        self.assertEqual(all_chairs.magnitude, 120)
        self.assertEqual(all_chairs.accuracy, 300.0)


        """ TODO
        Validating Invariants
        ---------------------

        The `IDvAmount` have two invariants:

        * The first one verifies if the accuracy is zero and is a percentage accuracy::

            >>> a_set_of_cars = Amount(magnitude=70,accuracy=0.0,accuracy_is_percent=True)
            >>> IDvAmount.validateInvariants(a_set_of_cars)
            Traceback (most recent call last):
            ...
            Invalid: The percentage accuracy cannot be zero. 

        * The second and last invariant check the percentage validity: it must be a
        value between 0 and 100::

            >>> a_set_of_computers = Amount(magnitude=70,accuracy=120.0,accuracy_is_percent=True)
            >>> IDvAmount.validateInvariants(a_set_of_computers)
            Traceback (most recent call last):
            ...
            Invalid: The percentage accuracy is not valid.
        """

class TestDvCount(unittest.TestCase):
    def test_constructor(self):
        c = DvCount(magnitude=9)
        self.assertEqual(type(c), DvCount)

    def testAdd(self):
        c1 = DvCount(3)
        c2 = DvCount(5)
        expected = DvCount(8)
        self.assertEqual(expected, c1 + c2)
        self.assertEqual(expected, c2 + c1)

    def testSubtract(self):
        c1 = DvCount(3)
        c2 = DvCount(5)
        expected = DvCount(2)
        self.assertEqual(expected, c2 - c1)

    def testCompareTo(self):
        c1 = DvCount(3)
        c2 = DvCount(5)
        c3 = DvCount(3)

        self.assertTrue(c1 < c2)
        self.assertTrue(c2 > c1)
        self.assertTrue(c3 == c1)
        self.assertTrue(c1 == c3)
    
    def testGetOtherReferenceRanges(self):
        normal = DvText(ReferenceRange.NORMAL)
        lower = DvCount(1)
        upper = DvCount(10)
        normalRange = ReferenceRange(normal, DvInterval(lower, upper))
        otherReferenceRanges = [normalRange]
        
        count = DvCount(other_reference_ranges=otherReferenceRanges, accuracy=0.0, accuracy_is_percent=False, magnitude=5)
        self.assertEqual(otherReferenceRanges, count.other_reference_ranges)


class TestDvInterval(unittest.TestCase):
        pass

class TestDvProportion(unittest.TestCase):
    def test_constructor(self):
        p = DvProportion(numerator=2, denominator=1, type=0, precision=-1)
        self.assertEqual(type(p), DvProportion)

class TestDvQuantity(unittest.TestCase):
    def test_constructor(self):
        qty = DvQuantity(magnitude=100.2, units="km/h", precision=-1)
        self.assertEqual(type(qty), DvQuantity)

class TestReferenceRange(unittest.TestCase):
    def test_constructor(self):
        tid = TerminologyID("SNOMED-CT(2003)")
        tid1 = TerminologyID("ISO_639-1")
        tid2 = TerminologyID("10646-1:1993")
        cpm = CodePhrase(tid, "abc123")
        tm = TermMapping(cpm, "=",None)
        cplang = CodePhrase(tid1, "en")
        cpenc = CodePhrase(tid2, "utf-8")
        uri = DvURI("http://www.mlhim.org")
        meaning = DvText("Some really interesting ReferenceRange.",[tm,],u"font-family:Arial",uri,cplang,cpenc)

        intvl = DvInterval(0, 10, lower_included=1, upper_included=1)
        rr = ReferenceRange(meaning=meaning, range=intvl)
        self.assertEqual(type(rr), ReferenceRange)


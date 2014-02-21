
from openehr.rm.datatypes.quantity.datetime import DvDuration, DvTemporal, DvDate, DvDateTime, DvTime

import unittest

class TestDvDate(unittest.TestCase):

    def testCompareTo(self):
        self.assertTrue(DvDate("1999-12-31") < DvDate("2000-01-01"))
        self.assertTrue(DvDate("2001-01-31") < DvDate("2001-02-01"))
        self.assertTrue(DvDate("2001-02-11") < DvDate("2001-02-12"))

        self.assertTrue(DvDate("20030201") > DvDate("20021215"))
        self.assertTrue(DvDate("20030202") > DvDate("20030124"))
        self.assertTrue(DvDate("20030216") > DvDate("20030215"))

        self.assertTrue(DvDate("2002-02") == DvDate("2002-02-01"))
        self.assertTrue(DvDate("2002-02") < DvDate("2002-02-02"))
        self.assertTrue(DvDate("2002") < DvDate("2002-02-02"))
        self.assertTrue(DvDate("2002-02") > DvDate("2002-01"))
        self.assertTrue(DvDate("2002") > DvDate("2001-12"))

    def testToString(self):
        self.assertEquals(str(DvDate("2001-01-15"), "2001-01-15"))
        self.assertEquals(str(DvDate("20011015"), "20011015"))
        self.assertEquals(str(DvDate("2001-10"), "2001-10"))
        self.assertEquals(str(DvDate("2001"), "2001"))
        self.assertEquals(str(DvDate(2001, 12, 15), "2001-12-15"))
        self.assertEquals(str(DvDate(2000, 10), "2000-10"))
        self.assertEquals(str(DvDate(2000), "2000"))

    def testEquals(self):
        #Two DvDate are equal if both indicate the same date.
        dateOne = DvDate("2004-01-31")
        dateTwo = DvDate(2004, 1, 31)
        dateThree = DvDate("20040131")
        self.assertTrue(dateOne == dateTwo)
        self.assertTrue(dateTwo == dateOne)
        self.assertTrue(dateOne == dateThree)
        self.assertTrue(dateThree == dateOne)
        self.assertTrue(dateTwo == dateThree)
        self.assertTrue(dateThree == dateTwo)

        dateOne = DvDate("1999-09")
        dateTwo = DvDate(1999, 9)
        dateThree = DvDate("199909")
        self.assertTrue(dateOne == dateTwo)
        self.assertTrue(dateTwo == dateOne)
        self.assertTrue(dateOne == dateThree)
        self.assertTrue(dateThree == dateOne)
        self.assertTrue(dateTwo == dateThree)
        self.assertTrue(dateThree == dateTwo)
    
    def testConstructorTakesString(self):
        values = [
            "2004-12-31", "1999-01-01", "18990102", "1789-09", "166612", "2002"
        ]
        for value in values:
            self.assertEquals(DvDate(value), DvDate(value))

    def testConstructorTakesIntegers(self):
        self.assertNotNull(DvDate(1000))
        self.assertNotNull(DvDate(1980, 11))


        self.assertNotNull(DvDate(2000, 11, 30))

    def testGetYearMonthDay(self):
        date = DvDate(1999, 10, 20)
        self.assertEquals(1999, date.year())
        self.assertEquals(10, date.month())
        self.assertEquals( 20, date.day())
        date = DvDate("2002-09-20")
        self.assertEquals(2002, date.year())
        self.assertEquals(9, date.month())
        self.assertEquals(20, date.day())
        date = DvDate("20060107")
        self.assertEquals(2006, date.year())
        self.assertEquals(1, date.month())
        self.assertEquals(7, date.day())
        date = DvDate("204611")
        self.assertEquals(2046, date.year())
        self.assertEquals(11, date.month())
        self.assertEquals(-1, date.day())
        date = DvDate(1988, 3)
        self.assertEquals(1988, date.year())
        self.assertEquals(3, date.month())
        self.assertEquals(-1, date.day())
        date = DvDate("2020")
        self.assertEquals(2020, date.year())
        self.assertEquals(-1, date.month())
        self.assertEquals(-1, date.day())

    def testMonthday_known(self):
        date = DvDate(1999, 10, 20)
        self.assertEquals(False, date.is_partial())
        self.assertEquals(True, date.month_known())
        self.assertEquals(True, date.day_known())
        date = DvDate("204611")
        self.assertEquals(True, date.is_partial())
        self.assertEquals(True, date.month_known())
        self.assertEquals(False, date.day_known())
        date = DvDate(2020)
        self.assertEquals(True, date.is_partial())
        self.assertEquals(False, date.month_known())
        self.assertEquals(False, date.day_known())
    
    def testSetValueInConstructor(self):
        self.assertEquals(DvDate(2).value, "0002")
        self.assertEquals(DvDate(20).value, "0020")
        self.assertEquals(DvDate(200).value, "0200")
        self.assertEquals(DvDate(2000).value, "2000")
        
        self.assertEquals(DvDate(2000, 9).value, "2000-09")
        self.assertEquals(DvDate(2000, 10).value, "2000-10")
        
        self.assertEquals(DvDate(2000, 10, 1).value, "2000-10-01")
        self.assertEquals(DvDate(2000, 10, 10).value, "2000-10-10")

class TestDvDuration(unittest.TestCase):

    def testConstructorTakesString(self):
        # test with wrong format
        values = [
            None, "P10D9H8m7s", "10", "", "P10D11WT9h8M7s", "P10a8m7s", "T9H8m0,000s",
            "P-1y-4W", "-P0Y0DT-7H", "PT", "P0DT" #/once T is there, must be followed by at least one time ele
        ]
        for value in values:
            with self.assertRaise(Exception):
                DvDuration(value)

        # test with expected values
        values = [
            "P0Y12M32W10DT9H8m7.898s", "P10DT9H8m7s",
            "P10D", "PT9H", "PT8m", "PT7s",
            "P10DT9H", "PT9H8m", "PT8m7s", "P10DT7s",
            "P10DT9H7s", "PT9H0M8S", "P1Y2M3W4D",
            "P9y6dT2.99s", "P35WT45H", "P20M33DT79m",
            "PT0,19s", "-P1Y2m3W4dT5H6m7,8s",
            "-PT0H0m56s", "P", "P0Y", "P0DT0s", "PT0H",
            "PT0s"
        ]
        data = [
            (0, 12, 32, 10, 9, 8, 7, 898), (0, 0, 0, 10, 9, 8, 7, 0),
            (0, 0, 0, 10, 0, 0, 0, 0), (0, 0, 0, 0, 9, 0, 0, 0), (0, 0, 0, 0, 0, 8, 0, 0), 
            (0, 0, 0, 0, 0, 0, 7, 0), (0, 0, 0, 10, 9, 0, 0, 0),
            (0, 0, 0, 0, 9, 8, 0, 0), (0, 0, 0, 0, 0, 8, 7, 0), 
            (0, 0, 0, 10, 0, 0, 7, 0), (0, 0, 0, 10, 9, 0, 7, 0), 
            (0, 0, 0, 0, 9, 0, 8, 0), (1, 2, 3, 4, 0, 0, 0, 0),
            (9, 0, 0, 6, 0, 0, 2, 990), (0, 0, 35, 0, 45, 0, 0, 0),
            (0, 20, 0, 33, 0, 79, 0, 0), (0, 0, 0, 0, 0, 0, 0, 190),
            (-1, -2, -3, -4, -5, -6, -7, -800), (0, 0, 0, 0, 0, 0, -56, 0),
            (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0)
        ]
        for i, value in enumerate(values):
            self.assertDuration(value, data[i])

    def assertDuration(self, value, data):
        d = DvDuration(value)
        self.assertEquals(data[0], d.years())
        self.assertEquals(data[1], d.months())
        self.assertEquals(data[2], d.weeks())
        self.assertEquals(data[3], d.days())
        self.assertEquals(data[4], d.hours())
        self.assertEquals(data[5], d.minutes())
        self.assertEquals(data[6], d.seconds())
        self.assertEquals(data[7], (int)(d.fractional_seconds()*1000.0))

    def testConstructorTakesIntegers(self):
        datasets = [
            [0, 10, 3, 1, 19, 8, 37, 857], [0, 0, 0, 1, 0, 14, 2, 0],
            [0, 13, 56, 33, 25, 67, 77, 0], [0, -1, -2, 0, -9, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 10, 9, 0, 0, 0],
        ]
        for i, data in enumerate(datasets):
            d = DvDuration(data)
            self.assertEquals("years", data[ 0 ], d.years())
            self.assertEquals("months", data[ 1 ], d.months())
            self.assertEquals("weeks", data[ 2 ], d.weeks())
            self.assertEquals("days", data[ 3 ], d.days())
            self.assertEquals("hours", data[ 4 ], d.hours())
            self.assertEquals("minutes", data[ 5 ], d.minutes())
            self.assertEquals("seconds", data[ 6 ], d.seconds())
            self.assertEquals("fseconds", data[ 7 ], (int)(d.fractional_seconds()*1000.0))

        fData = [
            [0, 0, 3, 1, 0, 8, 37, 1857], [0, 0, 0, -1, 0, 14, 2, 0],      
        ]
        for i, data in enumerate(fData):
            with self.self.assertRaises(Exception):
                d = DvDuration(data)

    def testAdd(self):
        one = DvDuration(0, 0, 0, 10, 20, 30, 40, .5)
        two = DvDuration(0, 0, 1, 1, 2, 3, 4, .05)
        d = one + two
        
        self.assertEquals(0, d.years())
        self.assertEquals(0, d.months())
        self.assertEquals(2, d.weeks()) # //10d + 1W1d = 18d
        self.assertEquals(4, d.days()) # //18d = 2W4d
        self.assertEquals(22, d.hours())
        self.assertEquals(33, d.minutes())
        self.assertEquals(44, d.seconds())
        self.assertEquals(.55, d.fractional_seconds())
        
        three = DvDuration("P1y2WT2H10m1,60S")
        d = d + three
        self.assertEquals(1, d.years())
        self.assertEquals(1, d.months())# //33d = 1M2d
        self.assertEquals(0, d.weeks())
        self.assertEquals(2, d.days())
        self.assertEquals(0, d.hours())
        self.assertEquals(43, d.minutes())
        self.assertEquals(46, d.seconds())
        self.assertEquals(.15, d.fractional_seconds())

    def testSubtract(self):
        one = DvDuration(0, 0, 0, 10, 20, 30, 40, .5)
        two = DvDuration(0, 0, 1, 0, 2, 3, 4, .05)
        d = one - two
        #/System.out.println("after subtraction: " + d.toString())
        self.assertEquals(0, d.years())
        self.assertEquals(0, d.months())
        self.assertEquals(0, d.weeks())
        self.assertEquals(3, d.days())
        self.assertEquals(18, d.hours())
        self.assertEquals(27, d.minutes())
        self.assertEquals(36, d.seconds())
        self.assertEquals(.45, d.fractional_seconds())

        three = DvDuration("P5D")
        d = d.subtract(three)
        #/System.out.println("after second subtraction: " + d.toString())
        self.assertEquals(0, d.years())
        self.assertEquals(0, d.months())
        self.assertEquals(0, d.weeks())
        self.assertEquals(-1, d.days())
        self.assertEquals(-5, d.hours())
        self.assertEquals(-32, d.minutes())
        self.assertEquals(-23, d.seconds())
        self.assertEquals(-0.55, d.fractional_seconds())
        self.assertEquals("-P1DT5H32M23,550S", d.toString())

    def testToString(self):
        #/constructor takes string, integers, after addition/subtraction
        datasets = [
            [0, 0, 0, 10, 20, 30, 40, 0], [0, 0, 0, 1, 0, 14, 2, 0],
            [0, 13, 56, 33, 25, 67, 77, 0], [0, -1, -2, 0, -9, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0], [0, 11, 23, 10, 9, 5, 0, 123]
        ]
        strings = [
           "P10DT20H30M40S", "P1DT14M2S", "P13M56W33DT25H67M77S",
           "-P1M2WT9H", "PT0S", "P11M23W10DT9H5M0,123S"
        ]
        for i, data in enumerate(datasets):
            d = DvDuration(*data)
            self.assertEquals(strings[i], str(d))
        
        strValues = [
           "P10DT20H30M40.66S", "P16M45DT60M2S", "P13M56W33DT2H6M5.0S",
           "-P1M2WT9H", "PT0S", "P11M23W10DT9H5M0,123S", "P"]
        for i, svalue in enumerate(strValues):
            d = DvDuration(svalue)
            self.assertEquals(svalue, str(d))

    def testCompareTo(self):
        value = [1, 13, 45, 10, 20, 30, 40, 500] #/D=(2*365)+31+(45*7)+10
        d1 = DvDuration(*value)
        d2 = DvDuration(*value)
        self.assertTrue(d1 == d2)
        self.assertTrue(d2 == d1)

        array = [
            [1, 13, 45, 10, 20, 30, 40, 499], #/the next 3 sets are all equivalent to the first
            [2, 0, 0, 356, 20, 30, 40, 499], [2, 11, 0, 21, 20, 0, 220, 499],            
            [2, 11, 3, 0, 20, 30, 40, 499],
            [-2, -13, -45, -10, -20, -20, 0, -5], [0, 0, 0, 10, 10, 50, 40, 5],
        ]
        for i, value in enumerate(array):
            d = DvDuration(*value)
            self.assertTrue(d1 > d)
            self.assertTrue(d < d1)
    
    def testEquals(self):
        self.assertEquals(DvDuration("P1Y2M3W"), DvDuration(1, 2, 3, 0, 0, 0, 0, 0.0))
        self.assertEquals(DvDuration("-P1Y2M3DT25H6S"), DvDuration(-1, -2, 0, -3, -25, 0, -6, 0.0))
        self.assertEquals(DvDuration("PT6H220m89.719S"), DvDuration(0, 0, 0, 0, 6, 220, 89, .719))
        self.assertEquals(DvDuration("P"), DvDuration(0, 0, 0, 0, 0, 0, 0, 0.0))


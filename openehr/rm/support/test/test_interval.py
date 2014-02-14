from openehr.rm.support import Interval, Smallest, Largest
import unittest

class TestInterval(unittest.TestCase):

    def testConstructor(self):
        self.assertNotEqual(Interval(1, 10), None)
        with self.assertRaises(ValueError):
            Interval(10, 1)

    def testHas(self):
        # array of { lower, upper,
        #            lower_inclusive, upper_inclusive 
        #            testValue, expected }
        data = [
            # inclusive boundaries
            [1, 8, True, True, 2, True],
            [1, 8, True, True, 1, True],
            [1, 8, True, True, 8, True],
            [1, 8, True, True, 0, False],
            [1, 8, True, True, 9, False],
            [Smallest(), 8, False, True, 4, True],
            [Smallest(), 8, False, True, -1, True],
            [Smallest(), 8, False, True, 9, False],
            [1, Largest(), True, False, 4, True],
            [1, Largest(), True, False, 1, True],
            [1, Largest(), True, False, -1, False],
            # exclusive boundaries
            [1, 8, False, False, 2, True],
            [1, 8, False, False, 1, False],
            [1, 8, False, False, 8, False],
            [1, 8, False, False, 0, False],
            [1, 8, False, False, 9, False],
            [Smallest(), 8, False, False, 4, True],
            [Smallest(), 8, False, False, -1, True],
            [Smallest(), 8, False, False, 9, False],
            [1, Largest(), False, False, 4, True],
            [1, Largest(), False, False, 1, False],
            [1, Largest(), False, False, -1, False]
        ]

        for lower, upper, lower_inclusive, upper_inclusive, test_value, expected in data:
            iv = Interval(lower, upper, lower_inclusive, upper_inclusive)
            self.assertEqual(iv.has(test_value), expected)

    def testEquals(self):
        interval = Interval(-1, 10)
        interval2 = Interval(-1, 10)
        self.assertEqual(interval, interval2)

        interval = Interval(-1, 10, True, False)
        interval2 = Interval(-1, 10, True, False)
        self.assertEqual(interval, interval2);

        interval = Interval(-1, 10, True, False)
        interval2 = Interval(-1, 10, True, True);
        self.assertFalse(interval == interval2)
        self.assertNotEqual(interval, interval2)

        # not equals expected
        data = [ (-1, 9), (2, 10), (0, 10), (-1, 0), (0, 0) ]

        for row in data:
            interval2 = Interval(row[0], row[1])
            self.assertFalse(interval == interval2)
            self.assertFalse(interval2 == interval)

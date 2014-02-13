from openehr.rm.support.identification import VersionTreeID, InvalidUID
import unittest
    
class TestVersionTreeID(unittest.TestCase):

    def testConstructors(self):
        values = [ "1.1.2", "2", "1.3.24", "10", "3.0.0" ]
        intS = [
            [1, 1, 2],
            [2, 0, 0],
            [1, 3, 24],
            [10, 0, 0],
            [3, 0, 0]
        ]
        isB = [ True, False, True, False, False ]
                
        for i, value in enumerate(values):
            v1 = VersionTreeID(value)
            v2 = VersionTreeID(intS[i][0], intS[i][1], intS[i][2])
            self.assertEqual(v1, v2)

            bN = None if intS[i][1] == 0 else str(intS[i][1])
            bV = None if intS[i][2] == 0 else str(intS[i][2])

            self.assertEqual(str(intS[i][0]), v2.trunk_version())
            self.assertEqual(bN, v2.branch_number())
            self.assertEqual(bV, v2.branch_version())
            self.assertEqual(isB[i], v2.is_branch())
    
    def testConstructorsFail(self):
        values = [ "1.0.2", "0", "0.3.24", "1.1.0", "0.0.0", "1.1" ]
        intS = [
            [0, 1, 2],
            [0, 0, 0],
            [1, 3, 0],
            [10, 0, 1], 
            [-1, 3, 2], 
            [1, -2, 2]
        ]
        for value in values:
            with self.assertRaises(InvalidUID):
                VersionTreeID(value)
        for int_value in intS:
            with self.assertRaises(InvalidUID):
                VersionTreeID(*int_value)
    
    def testIsFirst(self):
        
        values = ["1", "1.0.0", "1.1.1", "2"]
        iF = [True, True, False, False]
        for i in range(len(values)):
            self.assertEquals(iF[i], VersionTreeID(values[i]).is_first())

    def testNext(self):
        values = ["1", "1.0.0", "1.1.1", "2"]
        nextV = ["2", "2", "1.1.2", "3"]
        for i in range(len(values)):
            self.assertEquals(VersionTreeID(nextV[i]), VersionTreeID(values[i]).is_first())

    def testToString(self):
        intS = [
            [1, 1, 2],
            [1, 0, 0],
            [1, 3, 1],
        ]
        values = [ "1.1.2", "1", "1.3.1" ]
        for i in range(len(values)):
            self.assertEqual(values[i],
                str(VersionTreeID(intS[i][0], intS[i][1], intS[i][2])))

        tValues = [ "1.1.2", "1", "1.0.0", "2.0.0" ]
        eValues = [ "1.1.2", "1", "1", "2" ]
        for i in range(len(values)):
            self.assertEqual(eValues[i], str(VersionTreeID(tValues[i])))

import unittest
import sys
from datetime import datetime
from datetime import date
from script import generateInitialData, reset, lookup, dateToCompare, validAge, birthBeforeMarriage2, siblingAgeDiff

gedcomStructuredData    = generateInitialData("gedFiles/birthBeforeMarriage2before.ged") #store the tables and lists into gedcomStructuredData
indiList_bbm2b		= gedcomStructuredData['indiList']
famList_bbm2b		= gedcomStructuredData['famList']
reset()

gedcomStructuredData    = generateInitialData("gedFiles/birthBeforeMarriage2after.ged") #store the tables and lists into gedcomStructuredData
indiList_bbm2a		= gedcomStructuredData['indiList']
famList_bbm2a		= gedcomStructuredData['famList']
reset()

gedcomStructuredData    = generateInitialData("family_project.ged") #store the tables and lists into gedcomStructuredData
indiList_normal		= gedcomStructuredData['indiList']
famList_normal		= gedcomStructuredData['famList']
reset()

gedcomStructuredData    = generateInitialData("gedFiles/SiblingAgeDiff.ged") #store the tables and lists into gedcomStructuredData
indiList_badSiblingAgeDiff		= gedcomStructuredData['indiList']
famList_badSiblingAgeDiff		= gedcomStructuredData['famList']
reset()

class TestAge(unittest.TestCase):
    def test_validAge(self):
        result = validAge(0)
        self.assertTrue(result)
        result = validAge(27)
        self.assertTrue(result)
        result = validAge(82)
        self.assertTrue(result)
        result = validAge(150)
        self.assertFalse(result)
        result = validAge(184)
        self.assertFalse(result)
        result = validAge(21345)
        self.assertFalse(result)
        
    def test_birthBeforeMarriage2(self):
        result = birthBeforeMarriage2(famList_bbm2a, indiList_bbm2a)
        self.assertFalse(result)
        result = birthBeforeMarriage2(famList_bbm2b, indiList_bbm2b)
        self.assertFalse(result)
        result = birthBeforeMarriage2(famList_normal, indiList_normal)
        self.assertTrue(result)
        
    def test_siblingAgeDiff(self):
        result = siblingAgeDiff(famList_normal, indiList_normal)
        self.assertTrue(result)
        result = siblingAgeDiff(famList_badSiblingAgeDiff, indiList_badSiblingAgeDiff)
        self.assertFalse(result)

if __name__ == "__main__":
    # test_classes_to_run = [TestClassA, TestClassC]
    # loader = unittest.TestLoader()
    suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
    unittest.TextTestRunner(verbosity=3).run( suite )

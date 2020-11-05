import unittest
import sys
from datetime import datetime
from datetime import date
from script import generateInitialData, reset, lookup, dateToCompare, validAge, birthBeforeMarriage2, siblingAgeDiff, childParentAgeDiff, largestFamily

gedcomStructuredData    = generateInitialData("gedFiles/invalidAge.ged") #store the tables and lists into gedcomStructuredData
indiList_invalidAge		= gedcomStructuredData['indiList']
famList_invalidAge		= gedcomStructuredData['famList']
reset()

gedcomStructuredData    = generateInitialData("gedFiles/birthBeforeMarriage2before.ged") #store the tables and lists into gedcomStructuredData
indiList_bbm2b		= gedcomStructuredData['indiList']
famList_bbm2b		= gedcomStructuredData['famList']
reset()

gedcomStructuredData    = generateInitialData("gedFiles/birthBeforeMarriage2before.ged") #store the tables and lists into gedcomStructuredData
indiList_bbm2b		= gedcomStructuredData['indiList']
famList_bbm2b		= gedcomStructuredData['famList']
reset()

gedcomStructuredData    = generateInitialData("gedFiles/birthBeforeMarriage2after.ged") #store the tables and lists into gedcomStructuredData
indiList_bbm2a		= gedcomStructuredData['indiList']
famList_bbm2a		= gedcomStructuredData['famList']
reset()

gedcomStructuredData    = generateInitialData("gedFiles/normal.ged") #store the tables and lists into gedcomStructuredData
indiList_normal		= gedcomStructuredData['indiList']
famList_normal		= gedcomStructuredData['famList']
reset()

gedcomStructuredData    = generateInitialData("gedFiles/SiblingAgeDiff.ged") #store the tables and lists into gedcomStructuredData
indiList_badSiblingAgeDiff		= gedcomStructuredData['indiList']
famList_badSiblingAgeDiff		= gedcomStructuredData['famList']
reset()

gedcomStructuredData    = generateInitialData("gedFiles/ParentChildAgeDiff.ged") #store the tables and lists into gedcomStructuredData
indiList_invalidParChildAgeDiff		= gedcomStructuredData['indiList']
famList_invalidParChildAgeDiff		= gedcomStructuredData['famList']
reset()

gedcomStructuredData    = generateInitialData("gedFiles/family_projectjared.ged") #store the tables and lists into gedcomStructuredData
indiList_jared		= gedcomStructuredData['indiList']
famList_jared		= gedcomStructuredData['famList']
reset()

class TestAge(unittest.TestCase):
    def test_validAge(self):
        result = validAge(indiList_invalidAge)
        self.assertFalse(result)
        result = validAge(indiList_normal)
        self.assertTrue(result)
        
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
        
    def test_childParentAgeDiff(self):
        result = childParentAgeDiff(famList_normal, indiList_normal)
        self.assertTrue(result)
        result = childParentAgeDiff(famList_invalidParChildAgeDiff, indiList_invalidParChildAgeDiff)
        self.assertFalse(result)
        
    def test_largestFamily(self):
        result = largestFamily(famList_normal)
        self.assertEqual(result, 'f32')
        result = largestFamily(famList_jared)
        self.assertEqual(result, 'F10')

if __name__ == "__main__":
    # test_classes_to_run = [TestClassA, TestClassC]
    # loader = unittest.TestLoader()
    suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
    unittest.TextTestRunner(verbosity=3).run( suite )

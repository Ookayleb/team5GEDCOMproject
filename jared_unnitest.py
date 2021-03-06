import unittest
import pandas as pd
import sys
from datetime import datetime
from datetime import date
from script import generateInitialData, reset, lookup, dateToCompare, validAge, birthBeforeMarriage2, siblingAgeDiff, childParentAgeDiff, largestFamily, get_living_single, get_large_age_diff, get_children_same_birthdays, get_children_named_after_parent

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

gedcomStructuredData    = generateInitialData("gedFiles/large_age_diff.ged") #store the tables and lists into gedcomStructuredData
indiList_large_age_diff		= gedcomStructuredData['indiList']
famList_large_age_diff		= gedcomStructuredData['famList']
reset()

gedcomStructuredData    = generateInitialData("gedFiles/children_same_bday.ged") #store the tables and lists into gedcomStructuredData
indiList_children_same_bday		= gedcomStructuredData['indiList']
famList_children_same_bday		= gedcomStructuredData['famList']
reset()

gedcomStructuredData    = generateInitialData("gedFiles/named_after_parent.ged") #store the tables and lists into gedcomStructuredData
indiList_named_after_parent  	= gedcomStructuredData['indiList']
famList_named_after_parent		= gedcomStructuredData['famList']
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
        
    def test_large_agg_diff(self):
        large_age_list = []
        result = get_large_age_diff(indiList_normal, famList_normal)
        self.assertEqual(result,large_age_list)
        large_age_list = [['Bob /Smith/', 'Sarah /Smith/']]
        result = get_large_age_diff(indiList_large_age_diff, famList_large_age_diff)
        self.assertTrue(result,large_age_list)
        
    def test_living_single(self):
        living_single = ['Ann /Smith/', 'Jake /Smith/']
        result = get_living_single(indiList_normal, famList_normal)
        self.assertEqual(result,living_single)
        living_single = ['James /Middleton/', 'Kayla /Middleton/', 'Alex /Middleton/']
        result = get_living_single(indiList_jared, famList_jared)
        self.assertTrue(result,living_single)
        
    def test_get_children_same_birthdays(self):
        same_bday = [['I40', 'I43'], ['I48', 'I49']]
        result = get_children_same_birthdays(indiList_children_same_bday, famList_children_same_bday)
        self.assertEqual(result,same_bday)
        same_bday = []
        result = get_children_same_birthdays(indiList_normal, famList_normal)
        self.assertEqual(result,same_bday)
        
    def test_get_children_named_after_parent(self):
        named_after = ['I43', 'I48']
        result = get_children_named_after_parent(indiList_named_after_parent, famList_named_after_parent)
        self.assertEqual(result,named_after)
        named_after = []
        result = get_children_named_after_parent(indiList_normal, famList_normal)
        self.assertEqual(result,named_after)


if __name__ == "__main__":
    # test_classes_to_run = [TestClassA, TestClassC]
    # loader = unittest.TestLoader()
    suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
    unittest.TextTestRunner(verbosity=3).run( suite )

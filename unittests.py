import unittest
import sys
from script import validDate, check_gender_roles, check_unique_child, isDateLegitimate, check_dupe_spouses
from script import birthBeforeMarriage, reset, generateInitialData

class TestDates(unittest.TestCase):
    def test_success(self):
        result = validDate("15 OCT 2019")
        self.assertTrue(result)
        result = validDate("27 SEP 2020")
        self.assertTrue(result)

    def test_fail(self):
        result = validDate("15 OCT 2021")
        self.assertFalse(result)
        result = validDate("28 SEP 2021")
        self.assertFalse(result)

    def test_input_fail(self):
        with self.assertRaises(ValueError): validDate("15")

class TestBirthBeforeMarriage(unittest.TestCase):
    def test_success(self):
        print("Testing Birth Before Marriage Success")
        reset()
        gedcomStructuredData    = generateInitialData("gedFiles/0BirthAfterDeath.ged") #store the tables and lists into gedcomStructuredData
        famList_0warnings		= gedcomStructuredData['famList']
        result = birthBeforeMarriage(famList_0warnings)
        self.assertTrue(result)

    def test_fail(self):
        print("Testing Birth Before Marriage Failure")
        reset()
        gedcomStructuredData    = generateInitialData("gedFiles/2BirthAfterMarriage.ged") #store the tables and lists into gedcomStructuredData
        famList_2warnings		= gedcomStructuredData['famList']
        result = birthBeforeMarriage(famList_2warnings)
        self.assertFalse(result)

class TestGenderRoles(unittest.TestCase):
    def test_success(self):
        print("Testing Gender Roles Success")
        reset()
        gedcomStructuredData    = generateInitialData("family_project.ged") #store the tables and lists into gedcomStructuredData
        famList		= gedcomStructuredData['famList']
        result = check_gender_roles(famList)
        self.assertTrue(result)
        
    def test_failure(self):
        print("Testing Gender Roles Failure")
        reset()
        gedcomStructuredData    = generateInitialData("gedFiles/WrongGenders.ged") #store the tables and lists into gedcomStructuredData
        famList		= gedcomStructuredData['famList']
        result = check_gender_roles(famList)
        self.assertFalse(result)

class TestUniqueChild(unittest.TestCase):
    def test_success(self):
        print("Testing Unique Child Success")
        reset()
        gedcomStructuredData    = generateInitialData("family_project.ged") #store the tables and lists into gedcomStructuredData
        famList		= gedcomStructuredData['famList']
        result = check_unique_child(famList)
        self.assertTrue(result)

    def test_failure(self):
        print("Testing Unique Child Failure")
        reset()
        gedcomStructuredData    = generateInitialData("gedFiles/NoUniqueChildren.ged") #store the tables and lists into gedcomStructuredData
        famList		= gedcomStructuredData['famList']
        result = check_unique_child(famList)
        self.assertFalse(result)

class TestLegitDate(unittest.TestCase):
    def test_success(self):
        print("Testing Legit Date Success")
        result = isDateLegitimate("8 NOV 2020")
        self.assertTrue(result)
        
    def test_failure(self):
        print("Testing Legit Date Failure")
        result = isDateLegitimate("31 NOV 2020")
        self.assertFalse(result)
class TestDupeSpouses(unittest.TestCase):
    def test_success(self):
        print("Testing Dupe Spouses Success")
        reset()
        gedcomStructuredData    = generateInitialData("family_project.ged") #store the tables and lists into gedcomStructuredData
        famList		= gedcomStructuredData['famList']
        result = check_dupe_spouses(famList)
        self.assertTrue(result)

    def test_failure(self):
        print("Testing Dupe Spouses Failure")
        reset()
        gedcomStructuredData    = generateInitialData("gedFiles/dupeSpouses.ged") #store the tables and lists into gedcomStructuredData
        famList		= gedcomStructuredData['famList']
        result = check_dupe_spouses(famList)
        self.assertFalse(result)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
    unittest.TextTestRunner(verbosity=3).run( suite )

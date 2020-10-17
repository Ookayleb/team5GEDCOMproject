import unittest
import script
from script import get_deceased_records, generateInitialData, reset, get_parents_not_too_old, get_age_difference, replace_id_with_children_data, get_individual_age

class TestGetDeceasedRecords(unittest.TestCase):
	def test_get_deceased_records_1(self):
		reset()
		gedcomStructuredData = generateInitialData("gedFiles/Choy_family.ged")
		indiList = gedcomStructuredData['indiList']
		reset()
		result = get_deceased_records(indiList)[0]
		self.assertEqual(result, 1)

	def test_get_deceased_records_2(self):
		reset()
		gedcomStructuredData = generateInitialData("gedFiles/Choy_family.ged")
		indiList = gedcomStructuredData['indiList']
		reset()
		result = get_deceased_records(indiList)[1]
		self.assertTrue(result)



class TestGetParentsNotTooOld(unittest.TestCase):
	def test_get_parents_not_too_old_1(self):
		reset()
		gedcomStructuredData = generateInitialData("gedFiles/Choy_family.ged")
		famList	= gedcomStructuredData['famList']
		reset()
		result = get_parents_not_too_old(famList)[0]
		self.assertEqual(result, 1)

	def test_get_parents_not_too_old_2(self):
		reset()
		gedcomStructuredData = generateInitialData("gedFiles/Choy_family.ged")
		famList	= gedcomStructuredData['famList']
		reset()
		result = get_parents_not_too_old(famList)[1]
		self.assertTrue(result)

	def test_get_age_difference(self):
		self.assertEqual(get_age_difference(120, 70), 50)

	def test_replace_id_with_children_data(self):
		reset()
		gedcomStructuredData = generateInitialData("gedFiles/Choy_family.ged")
		famList	= gedcomStructuredData['famList']
		reset()

		for i in range(len(famList)):
			result = replace_id_with_children_data([famList[i]['Children']])
		self.assertTrue(result)



class TestGetIndividualAge(unittest.TestCase):
	def test_get_individual_ages(self):
		reset()
		gedcomStructuredData = generateInitialData("gedFiles/Choy_family.ged")
		indiList = gedcomStructuredData['indiList']
		reset()
		result = get_individual_age(indiList)
		self.assertTrue(result)



class TestGetLivingMarried(unittest.TestCase):
	def test_find_family_ids(self):
		reset()
		gedcomStructuredData = generateInitialData("gedFiles/Choy_family.ged")
		famList	= gedcomStructuredData['famList']
		reset()
		result = script.find_family_ids(famList)
		self.assertTrue(result)

	def test_get_married_list(self):
		reset()
		gedcomStructuredData = generateInitialData("gedFiles/Choy_family.ged")
		famList	= gedcomStructuredData['famList']
		reset()
		result = script.get_married_list(famList)
		self.assertTrue(result)

	def test_get_living_married(self):
		reset()
		gedcomStructuredData = generateInitialData("gedFiles/Choy_family.ged")
		indiList = gedcomStructuredData['indiList']
		reset()
		famList	= gedcomStructuredData['famList']
		reset()
		result = script.get_living_married(indiList, famList)
		self.assertTrue(result)


if __name__ == '__main__':
	unittest.main()
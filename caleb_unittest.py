import unittest
import sys
from script import validDate, check_dateOrder, reset, generateInitialData, verifyBirthDeathDateOrder, verifyMarriageDivorceOrder, verifyBigamy, verifyNoFirstCousinMarr


class TestDateOrder(unittest.TestCase):
	def test_birthBeforeDeath(self):
		result = check_dateOrder("15 OCT 2020", "15 OCT 2021")
		self.assertTrue(result)

	def test_deathBeforeBirth(self):
		result = check_dateOrder("15 OCT 2020", "15 OCT 2019")
		self.assertFalse(result, "Earlier year failed")
		result = check_dateOrder("15 OCT 2020", "15 SEP 2020")
		self.assertFalse(result, "Earlier month failed")
		result = check_dateOrder("15 OCT 2020", "14 OCT 2020")
		self.assertFalse(result, "Earlier day failed")
		result = check_dateOrder("15 OCT 2020", "14 SEP 2019")
		self.assertFalse(result, "Earlier year, month, and day failed")

	def test_birthWithNoDeath(self):
		result = check_dateOrder("15 OCT 2020", None)
		self.assertTrue(result)

	def test_birthEqualsDeath(self):
		result = check_dateOrder("15 OCT 2020", "15 OCT 2020")
		self.assertTrue(result)

	def test_deathWithNoBirth(self):
		result = check_dateOrder(None, "15 OCT 2021")
		self.assertFalse(result)


class TestVerifyBirthDeathDateOrder(unittest.TestCase):
	def test_0BirthAfterDeath(self):
		reset()
		gedcomStructuredData	= generateInitialData("gedFiles/0BirthAfterDeath.ged") #store the tables and lists into gedcomStructuredData
		indiList				= gedcomStructuredData['indiList']
		result 				= verifyBirthDeathDateOrder(indiList)
		self.assertEqual(result, 0)

	def test_2BirthAfterDeath(self):
		reset()
		gedcomStructuredData	= generateInitialData("gedFiles/2BirthAfterDeath.ged") #store the tables and lists into gedcomStructuredData
		indiList				= gedcomStructuredData['indiList']
		result 				= verifyBirthDeathDateOrder(indiList)
		self.assertEqual(result, 2)


class TestVerifyMarriageDivorceDateOrder(unittest.TestCase):
	def test_0MarriageAfterDivorce(self):
		reset()
		gedcomStructuredData	= generateInitialData("gedFiles/0MarrAfterDiv.ged") #store the tables and lists into gedcomStructuredData
		famList				= gedcomStructuredData['famList']
		result 				= verifyMarriageDivorceOrder(famList)
		self.assertEqual(result, 0)

	def test_2MarriageAfterDivorce(self):
		reset()
		gedcomStructuredData	= generateInitialData("gedFiles/2MarrAfterDiv.ged") #store the tables and lists into gedcomStructuredData
		famList				= gedcomStructuredData['famList']
		result 				= verifyMarriageDivorceOrder(famList)
		self.assertEqual(result, 2)


class TestVerifyBigamy(unittest.TestCase):
	def test_4Bigamy(self):
		reset()
		gedcomStructuredData	= generateInitialData("gedFiles/allTest.ged") #store the tables and lists into gedcomStructuredData
		famList				= gedcomStructuredData['famList']
		famDF				= gedcomStructuredData['famDF']
		indiDF				= gedcomStructuredData['indiDF']
		result 				= verifyBigamy(famList, famDF, indiDF)
		self.assertEqual(result, 4)

	def test_0Bigamy(self):
		reset()
		gedcomStructuredData	= generateInitialData("gedFiles/Choy_familyTree.ged") #store the tables and lists into gedcomStructuredData
		famList				= gedcomStructuredData['famList']
		famDF				= gedcomStructuredData['famDF']
		indiDF				= gedcomStructuredData['indiDF']
		result 				= verifyBigamy(famList, famDF, indiDF)
		self.assertEqual(result, 0)


class TestVerifyNoFirstCousinMarr(unittest.TestCase):
	def test_FirstCousinMarriage(self):
		reset()
		gedcomStructuredData	= generateInitialData("gedFiles/cousinMarriage.ged") #store the tables and lists into gedcomStructuredData
		indiList				= gedcomStructuredData['indiList']
		famList				= gedcomStructuredData['famList']
		result 				= verifyNoFirstCousinMarr(indiList, famList)
		self.assertEqual(result, 1)

	def test_NoFirstCousinMarriage(self):
		reset()
		gedcomStructuredData	= generateInitialData("gedFiles/Choy_familyTree.ged") #store the tables and lists into gedcomStructuredData
		indiList				= gedcomStructuredData['indiList']
		famList				= gedcomStructuredData['famList']
		result 				= verifyNoFirstCousinMarr(indiList, famList)
		self.assertEqual(result, 0)


if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
	unittest.TextTestRunner(verbosity=3).run( suite )

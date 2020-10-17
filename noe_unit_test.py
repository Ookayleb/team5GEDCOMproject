import unittest
from script import generateInitialData, reset, get_age_difference,get_deceased_records, get_parents_not_too_old, getChildren_and_age, lookup

gedcomeStructuredData = generateInitialData("family_project.ged")
indiList = 	gedcomeStructuredData['indiList']
arr = []
for record in indiList:
	arr.append(record['ID'])
reset()


famiList = gedcomeStructuredData['famList']
reset()

class noe_unit_test(unittest.TestCase):
	def test_getChildren_and_age(self):
		self.assertTrue(getChildren_and_age(arr[0]))
		self.assertTrue(getChildren_and_age(arr[1]))
		self.assertTrue(getChildren_and_age(arr[2]))
		
	def test_get_age_difference(self):
		self.assertEqual(get_age_difference(75, 25), 50)
		self.assertNotEqual(get_age_difference(44, 20), 21)

	def test_get_deceased_records(self):
		self.assertTrue(get_deceased_records(indiList))
	
# gedcomeStructuredData2 = generateInitialData("family_project.ged")
# indiList2 = 	gedcomeStructuredData2['indiList'] 
# reset()

# gedcomeStructuredData3 = generateInitialData("family_project.ged")
# indiList3 = 	gedcomeStructuredData3['indiList']
# reset()

# gedcomeStructuredData4 = generateInitialData("family_project.ged")
# indiList4 = 	gedcomeStructuredData4['indiList']
# reset()

# gedcomeStructuredData5 = generateInitialData("family_project.ged")
# indiList5 = 	gedcomeStructuredData5['indiList']


# class GedcomTest(unittest.TestCase):

# 	def test_print_age_qualificationh(self):
# 		self.assertTrue(print_age_qualification(indiList1),
# 			[['Bobby Smith ', '1890-9-26', 'No'], ['Kate Smith ', '2012-7-05', 'Yes'], ['John Smith ', '2016-10-31', 'Yes']])
	
#     def test_print_age_qualificationh(self):
# 		self.assertTrue(print_age_qualification(indiList),[['Bobby Smith ', '1890-9-26', 'No'], ['Kate Smith ', '2012-7-05', 'Yes'], ['John Smith ', '2016-10-31', 'Yes']])

#     def test_print_age_qualificationh(self):
# 		self.assertTrue(print_age_qualification(indiList),
# 			[['Bobby Smith ', '1890-9-26', 'No'], ['Kate Smith ', '2012-7-05', 'Yes'], ['John Smith ', '2016-10-31', 'Yes']])

#     def test_print_age_qualificationh(self):
# 		self.assertTrue(print_age_qualification(indiList),
# 			[['Bobby Smith ', '1890-9-26', 'No'], ['Kate Smith ', '2012-7-05', 'Yes'], ['John Smith ', '2016-10-31', 'Yes']])

    # def test_get_deceased_records(self):
	# 	self.assertTrue(get_deceased_records(indiList))


if __name__ == '__main__':
	unittest.main()
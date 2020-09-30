import unittest
from script import generateInitialData, reset, print_age_qualification

gedcomeStructuredData1 = generateInitialData("family_project.ged")
indiList1 = 	gedcomeStructuredData1['indiList']
reset()

gedcomeStructuredData2 = generateInitialData("family_project.ged")
indiList2 = 	gedcomeStructuredData2['indiList']
reset()

gedcomeStructuredData3 = generateInitialData("family_project.ged")
indiList3 = 	gedcomeStructuredData3['indiList']
reset()

gedcomeStructuredData4 = generateInitialData("family_project.ged")
indiList4 = 	gedcomeStructuredData4['indiList']
reset()

gedcomeStructuredData5 = generateInitialData("family_project.ged")
indiList5 = 	gedcomeStructuredData5['indiList']


class GedcomTest(unittest.TestCase):

	def test_print_age_qualificationh(self):
		self.assertTrue(print_age_qualification(indiList1),
			[['Bobby Smith ', '1890-9-26', 'No'], ['Kate Smith ', '2012-7-05', 'Yes'], ['John Smith ', '2016-10-31', 'Yes']])
	
    def test_print_age_qualificationh(self):
		self.assertTrue(print_age_qualification(indiList),
			[['Bobby Smith ', '1890-9-26', 'No'], ['Kate Smith ', '2012-7-05', 'Yes'], ['John Smith ', '2016-10-31', 'Yes']])

    def test_print_age_qualificationh(self):
		self.assertTrue(print_age_qualification(indiList),
			[['Bobby Smith ', '1890-9-26', 'No'], ['Kate Smith ', '2012-7-05', 'Yes'], ['John Smith ', '2016-10-31', 'Yes']])

    def test_print_age_qualificationh(self):
		self.assertTrue(print_age_qualification(indiList),
			[['Bobby Smith ', '1890-9-26', 'No'], ['Kate Smith ', '2012-7-05', 'Yes'], ['John Smith ', '2016-10-31', 'Yes']])

    


if __name__ == '__main__':
	unittest.main()
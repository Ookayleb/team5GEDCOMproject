from script import generateInitialData, reset, print_age_qualification

gedcomeStructuredData = generateInitialData("family_project.ged")


indiDF = 	gedcomeStructuredData['indiDF']
famDF = 	gedcomeStructuredData['famDF']
indiList = 	gedcomeStructuredData['indiList']
famList = 	gedcomeStructuredData['famList']

class GedcomTest(unittest.TestCase):

	def test_print_age_qualificationh(self):
		self.assertTrue(print_age_qualification(indiList),
			[['Bobby Smith ', '1890-9-26', 'No'], ['Kate Smith ', '2012-7-05', 'Yes'], ['John Smith ', '2016-10-31', 'Yes']])
	


if __name__ == '__main__':
	unittest.main()
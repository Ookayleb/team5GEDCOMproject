# Jason Tran, William Martin, Caleb Choy, Jared Weinblatt, Sean James, Austin Luo, Noe Durocher
# I pledge my honor that I have abided by the Stevens Honor System
import sys
import re
import pandas as pd
from datetime import datetime
from datetime import date
import unittest
from prettytable import PrettyTable

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


#List of valid tags that should have Y for valid
VALID_TAGS = [
	'INDI',
	'NAME',
	'SEX',
	'BIRT',
	'DEAT',
	'FAMC',
	'FAMS',
	'FAM',
	'MARR',
	'HUSB',
	'WIFE',
	'CHIL',
	'DIV',
	'DATE',
	'HEAD',
	'TRLR',
	'NOTE'
]
#List of tags where the tag is the third token in a line
THIRD_TOKEN_TAGS =[
	'INDI',
	'FAM'
]

indiList 	= []		#will hold all individuals
famList	= []		#will hold all families

#US12-Parents not too old(father not 80 yrs older, and mother not 60 yrs older than child)****start

#helper function to calculate age difference fot get_parents_not_too_old() function
def get_age_difference(parent_age, child_age):
	age = parent_age - child_age
	return age

#function to print father, mother and children data and display if parents are too hold to be a child's parent
def get_parents_not_too_old(famList):
	family = []
	father_age_limit = 80
	mother_age_limit = 60
	father_too_old = ""
	mother_too_old = ""
	
	#loop to retrieve father, mother and children data from family record
	for i in range(len(famList)):
		try:
			family.append({'Husband_ID':famList[i]['Husband ID'], 'Wife_ID':famList[i]['Wife ID'],
				'Husband Name':famList[i]['Husband Name'], 'Wife Name':famList[i]['Wife Name'], 
				'Husband Age': lookup('Age', famList[i]['Husband ID']), 'Wife Age': lookup('Age', famList[i]['Wife ID']), 
				'Children': replace_id_with_children_data(famList[i]['Children'])})
		except:
			famList[i]['N/A'] = 'N/A'
			family.append({famList[i]['N/A']})

	table_arr = []

	# loop to build list to hold father, mother and children data
	for j in range(len(family)):
		for k in range(len(family[j]['Children'])):
			if(get_age_difference(family[j]['Husband Age'], family[j]['Children'][k]['Age']) > father_age_limit):
				father_too_old = "Yes"
			else:
				father_too_old = "No"

			if(get_age_difference(family[j]['Wife Age'], family[j]['Children'][k]['Age']) > mother_age_limit):
				mother_too_old = "Yes"
			else:
				mother_too_old = "No"

			table_arr.append([family[j]['Husband Name'],"Father", family[j]['Husband Age'],
				family[j]['Children'][k]['Name'], family[j]['Children'][k]['Gender'], family[j]['Children'][k]['Age'], father_too_old])
			table_arr.append([family[j]['Wife Name'], "Mother", family[j]['Wife Age'],
				family[j]['Children'][k]['Name'], family[j]['Children'][k]['Gender'], family[j]['Children'][k]['Age'], mother_too_old])


	#bring list to a prettytable structure
	x = PrettyTable()
	x.field_names = ['Parent Name', 'Relationship', 'Parent Age', 'Child Name', 'Sex', 'Child Age', 'Too old']
	for n in range(len(table_arr)):
		x.add_row([table_arr[n][0], table_arr[n][1], table_arr[n][2], 
			table_arr[n][3], table_arr[n][4], table_arr[n][5], table_arr[n][6]])
	print('\n\n')
	print('Parents not too old table\n')
	print(x)

	#************************************************************************end

#US29-Deceased list
def get_deceased_records(indList):
	print('Deceased list')
	print('\n')
	decease_list = {}
	id_arr = []
	name_arr = []
	gender_arr = []
	birth_arr = []
	age_arr = []
	death_arr = []
	spouse_arr = []
	for record in indList:
		if (record['Alive'] == False):
			id_arr.append(record['ID'])
			name_arr.append(record['Name'])
			gender_arr.append(record['Gender'])
			birth_arr.append(record['Birthday'])
			age_arr.append(record['Age'])
			death_arr.append(record['Death'])
			spouse_arr.append(record['Spouse'])

	decease_list['ID'] = id_arr
	decease_list['Name'] = name_arr
	decease_list['Gender'] = gender_arr
	decease_list['Birthday'] = birth_arr
	decease_list['Age'] = age_arr
	decease_list['Death'] = death_arr
	decease_list['Spouse'] = spouse_arr

	df = pd.DataFrame(decease_list, columns = ['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Death', 'Spouse'])
	print(df)
#***************************************************************************end

def test(indList):
	for i in indList:
		print( "****" + str(i))


#**********************************end
def print_age_qualification(indiList):

	#person = get_person_record()
	#one_hundred_and_thirty = get_exactly_130_years_of_age()
	each_person = []
	isQualified = ""

	for i in indiList:
		one_hundred_thirty = 130
		if (type(i['Age']) == int) :
			name_arr = i['Name']
			birth_day = i['Birthday']

			name = ""
			for j in range(len(name_arr)):
				name += name_arr[j].strip("/")
			if(i['Age'] <= one_hundred_thirty):
				isQualified = 'Yes'
				each_person.append([name, birth_day,  isQualified])
			else:
				isQualified = 'No'
				each_person.append([name, birth_day,  isQualified])
	return each_person

def print_data(indiList):
	person_record = print_age_qualification(indiList)
	n_arr = []
	b_arr = []
	q_arr = []
	person_data = {}
	for i in range(len(person_record)):
		n_arr.append(person_record[i][0])
		b_arr.append(person_record[i][1])
		q_arr.append(person_record[i][2])


	person_data['Name'] = n_arr
	person_data['Birth Date'] = b_arr
	person_data['Qualified'] = q_arr

	df = pd.DataFrame(person_data, columns = ['Name', 'Birth Date','Qualified'])
	return df




### HELPER FUNCTIONS ###
#Given an id and an attribute of intrest, returns the value of the attribute desired ex lookup("birthday", "I343628")
def lookup(attr, id):
	for indi in indiList:			#loop over all individuals
		if id == indi['ID']:		#if we find id
			return indi[attr]			#return the individual's data that we desire


#Calculate age given two dates. If death not supplied assume not dead
def calculateAge(born, death=False):
	if born is None:
		return 0
	born 	= datetime.strptime(born, "%d %b %Y")
	endDate 	= datetime.strptime(death, "%d %b %Y") if death else date.today() #if death is set, set end date as death. Otherwise, set end date as today
	return endDate.year - born.year - ((endDate.month, endDate.day) < (born.month, born.day))
	

# Checks date argument to see if that date is not after today's date
def validDate(arguments):
	current_date = date.today()
	try:
		date_arg = datetime.strptime(arguments, "%d %b %Y").date()
	except ValueError:
		raise ValueError("Incorrect data format, should be YYYY-MM-DD")

	if date_arg > current_date:
		return False
	return True

# Returns true if date1 is before date2,
def check_dateOrder(date1, date2):
	if (date1 is None):
		return False

	date1 = datetime.strptime(date1, "%d %b %Y")
	date2 = datetime.strptime(date2, "%d %b %Y") if date2 else None

	if date2 is None or date1 <= date2:
		return True
	else:
		return False

#function to find the children data
def getChildren_and_age(id):
	name = lookup('Name', id)
	age = lookup('Age', id)
	gender = lookup('Gender', id)
	return {'Name': name, 'Age':age, 'Gender':gender}

#function to replace the children id(s) with their actual data
def replace_id_with_children_data(children_arr):
	new_arr = []
	for i in range(len(children_arr)):
		new_arr.append(getChildren_and_age(children_arr[i]))
	return new_arr

#Verify that all death dates are after birth dates. Returns 0 if no offenders. If offenders detected, returns the number of them
def verifyBirthDeathDateOrder(indiList):
	print()
	print(indiList)
	print()
	print()
	for individual in indiList:
		if individual['Child'] != 'NaN':
			indiID = individual['ID']

			childBirthday = lookup("Birthday", indiID)
			childFamilyID = lookup("Child", indiID)

	print("birth" + childBirthday + "")

	warningList = []
	for i in indiList:
		if (check_dateOrder(i.get('Birthday', None), i.get('Death', None)) == False):
			warningList.append(i)

	warnDF = pd.DataFrame(warningList)
	if len(warnDF) < 1:
		print("No Death before Birth")
	else:
		print("WARNING: Death before Birth found:")
		print(pd.DataFrame(warningList))

	return len(warnDF)

#US16 SJ Sprint 1
def maleLastNames(indiDF, famList):
	lastNamesEqual = False
	childrenName = ''	#init child / husb name and childrenID
	husbandName = ''
	childrenID = ''
	malesList = indiDF[(indiDF['Gender'] == 'M')] #created list of males
	for fam in famList:
		# print(fam)
		husbandName = fam['Husband Name'] #for each family stor the husb name
		lastName = re.findall("\/(.*)\/", str(husbandName))[0]
		childrenID = fam['Children'] #get the childrenid
		# print('children ids', str(childrenID))
		# print('husband Last name' , str(lastName))
		for id in childrenID: #for all ids in childrenID
			#print('\n', str(id))
			malesID = malesList['ID'].to_list()
			if (id in malesID): #if child is in male list
				childrenName_bad = str(malesList.loc[malesList['ID'] == id, ['Name']])
				x = re.findall("\s*(\S*) \/(.*)\/", childrenName_bad)[0]
				childFirstName = x[0]
				childLastName 	= x[1]
				#print('Childs name is ' + childFirstName + ' ' + childLastName)
			else:
				#print ('Gender is ' + indiDF.loc[indiDF['ID'] == id, ['Gender'] ] + ' So do not check ')
				#Because it is a female so it does not matter what the last name is
				lastNamesEqual =True

			if(lastName == childLastName): #if the childs name contains the husbands name its true otherwise false
				#print('Family name is ' + lastName)
				lastNamesEqual = True

			else:
				print( '\n the name that doesnt match is ' + childFirstName + " " + childLastName)
				return False
	return lastNamesEqual

def validAge(age):
	if age >= 150:
		return False
	return True
	
#convert to datetime object
def dateToCompare(date):
	return datetime.strptime(date, "%d %b %Y")


def birthBeforeMarriage(famList):
	for family in famList:
		for childId in family["Children"]:
			marriageDate = dateToCompare(family['Married'])
			if childId != "NaN":
				birthday = dateToCompare(lookup("Birthday", childId))
				if marriageDate > birthday:
					return False
	return True

def siblingAgeDif(famList):
	for family in famList:
		if len(family["Children"]) > 1:
			dlow = dateToCompare(lookup("Birthday", family["Children"][0]))
			dhigh = dateToCompare(lookup("Birthday", family["Children"][0]))
			for childId in family["Children"]:
				birthday = dateToCompare(lookup("Birthday", childId))
				if birthday < dlow: 
					dlow=birthday
				if birthday > dhigh:
					dhigh=birthday
			ageDiff = dhigh.year - dlow.year - ((dhigh.month, dhigh.day) < (dlow.month, dlow.day))
			if ageDiff >= 35:
				return False
	return True


#Given a gedcom file, returns indi and fam tables, and also returns indi and fam lists.
def generateInitialData(fileName):
	with open(fileName, "r", encoding="utf8") as inFile:		#open the file provided in the argument
		line_num=-1
		for line in inFile:
			line_num+=1
			level		= ""
			tag			= ""
			valid		= ""
			arguments 	= ""
			tokenizedStr 	= re.search("(\d) (\S*) ?(.*)", line).groups()			#Use regex to store each token into a var. "1 NAME Bob /Smith/" becomes ["1", "NAME", "Bob /Smith/"]

			level	= tokenizedStr[0]

			#Check if third token is in the special list
			if tokenizedStr[2] in THIRD_TOKEN_TAGS:
				arguments	= tokenizedStr[1]	#if so, tag is actually the last token
				tag 		= tokenizedStr[2]	#arguments were the second argument
			else:
				tag 		= tokenizedStr[1]
				arguments	= tokenizedStr[2]

			#Valid is Y if we find the tag in the list of valid tags
			valid 	= 'N' if tag not in VALID_TAGS else 'Y'

			#Check for invalid tags
			if (tag=='DATE' and level=='1')  or  (tag=='NAME' and level=='2'):
				valid = 'N'
			if(tag == 'DATE'):
				if not validDate(arguments):
					raise Exception("No dates should be after the current date")


			if level == '0':
				if tag == "INDI":
					try:
						indiList[len(indiList) - 1] = newestIndiv
					except:
						pass
					newIndiv 			= {}
					newIndiv['ID'] 	= arguments
					newIndiv['Alive'] 	= True
					indiList.append(newIndiv)
				elif tag == "FAM":
					newFam 			= {}
					newFam['ID'] 		= arguments
					newFam['Children']	= []
					famList.append(newFam)


			elif level == '1':
				nextLineBirt 	= False
				nextLineDeat 	= False
				nextLineMarr 	= False
				newestIndiv 	= indiList[-1] if indiList else None	#This syntax chooses the the last element in indiList if it exists, otherwise the newestIndiv is None
				newestFam		= famList[-1] if famList else None
				if tag == "NAME":
					newestIndiv['Name'] 	= arguments
				elif tag == "SEX":
					newestIndiv['Gender'] 	= arguments
				elif tag == "BIRT":
					nextLineBirt 			= True
				elif tag == "DEAT":
					nextLineDeat 			= True
				elif tag == "MARR":
					nextLineMarr 			= True
				elif tag == "DIV":
					nextLineDiv			= True
				elif tag == "FAMS":
					newestIndiv['Spouse'] 	= arguments
				elif tag == "FAMC":
					newestIndiv['Child'] 	= arguments
				elif tag == "HUSB":
					newestFam['Husband ID'] 	= arguments
				elif tag == "WIFE":
					newestFam['Wife ID'] 	= arguments
				elif tag == "CHIL":
					newestFam['Children'].append(arguments)


			elif level == '2':
				newestIndiv 	= indiList[-1] if indiList else None
				newestFam		= famList[-1] if famList else None
				if nextLineBirt:
					newestIndiv['Birthday'] 	= arguments
					newestIndiv['Age'] 		= calculateAge(arguments)
				elif nextLineDeat:
					newestIndiv['Death'] 	= arguments
					newestIndiv['Age'] 		= calculateAge(newestIndiv.get('Birthday', None), arguments)
					newestIndiv['Alive'] 	= False
				elif nextLineMarr:
					newestFam['Married'] 	= arguments
				elif nextLineDiv:
					newestFam['Divorced'] 	= arguments


			#Code from Project 02
			# print("--> " + line.rstrip('\n'))
			# print("<-- " + level + "|" + tag + "|" + valid + "|" + arguments)


		#Populate the individuals DataFrame
		indiDF = pd.DataFrame(indiList, columns = ['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse'])
		indiDF["Age"] = pd.to_numeric(indiDF["Age"])
		indiDF.sort_values(by=['ID'], inplace=True)
		indiDF.reset_index(inplace=True, drop=True)

		#Check age of all individuals
		for i in range(len(indiList)):
			if not validAge(indiList[i]["Age"]):
				raise Exception(indiList[i]["Name"]+": Individuals must be less than 150 years old")

		#Populate the families DataFrame
		for i in range(len(famList)):		#Loop through the list of families
			famList[i]['Husband Name'] 	= lookup('Name', famList[i]['Husband ID']) #lookup husband name from id
			famList[i]['Wife Name'] 		= lookup('Name', famList[i]['Wife ID'])
		famDF = pd.DataFrame(famList, columns = ['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children'])
		famDF.sort_values(by=['ID'], inplace=True)
		famDF.reset_index(inplace=True, drop=True)


		#return a dictionary, whose keys are "indiDF", "famDF", "indiList", and "famList". Use this key value pair to obtain the actual dataframes or lists
		return {
			"indiDF": 	indiDF,
			"famDF":		famDF,
			"indiList":	indiList,
			"famList":	famList
		}

def reset():
	global indiList, famList
	indiDF = []
	indiList = []
	famDF = []
	famList = []







### MAIN CODE ###
def main():
	if(len(sys.argv) == 2):	#Check that we have 2 arguments
		gedcomStructuredData = generateInitialData(sys.argv[1]) #store the tables and lists into gedcomStructuredData

		indiDF = 		gedcomStructuredData['indiDF']
		famDF = 		gedcomStructuredData['famDF']
		indiList = 	gedcomStructuredData['indiList']
		famList = 	gedcomStructuredData['famList']
		
		# Now have access to indiDF and famDF DataFrames, can use below
		# Example template:
			# To print two columns of a table:
			# print(indiDF[['ID', 'Age']])
			#
			# To create a new table that has values that meet a certain criteria (Here our criteria is Age > 60 and Gender = M)
			# newTable = indiDF.loc[
			# 	(indiDF['Age']>60) & (indiDF['Gender'] == "M"),		#This line specifies the query
			# 	['Name','Age','Gender']							#This line specifies what columns our output contains. Is independent from the above line
			# ]
			# print(newTable)

		# CODE HERE


		def printIndi():
			print("Individuals")
			print(indiDF)

		def printFam():
			print("Families")
			print(famDF)

		# if not birthBeforeMarriage(famList):
		# 	print("All children must be born after marriage")
		# indiDF.to_csv("indiDF.csv", index=False)

		if not siblingAgeDif(famList):
			raise Exception("Sibling age difference must be less than 35 years")

		printIndi()
		print("\n\n")
		printFam()
		#test(indiList)
		get_deceased_records(indiList)
		print(print_data(indiList))
		get_parents_not_too_old(famList)
		#US16
		# if(maleLastNames(indiDF, famList)):
		# 	print("\n")
		# 	print('All males have same last name')
		# 	print("\n")
		# else:
		# 	print("\n")
		# 	print('All males do not have the same last name')
		# 	print("\n")

		#verifyBirthDeathDateOrder(indiList)
	else:
		print("Please provide a GEDCOM file.\nUSAGE: python3 script.py path/to/file.ged")

if __name__ == "__main__":
    # execute only if run as a script
    main()

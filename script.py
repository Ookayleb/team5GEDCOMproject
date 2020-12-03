# Jason Tran, William Martin, Caleb Choy, Jared Weinblatt, Sean James, Austin Luo, Noe Durocher
# I pledge my honor that I have abided by the Stevens Honor System
import sys
import re
import pandas as pd
import unittest
import numpy as np
from datetime import datetime
from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from prettytable import PrettyTable

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)



#---------------------### VARIABLES & CONSTANTS ###---------------------#
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

Colors = {
	"red": "\033[91m{}\033[00m",
	"red bold": "\033[1m\033[91m{}\033[00m",
	"green": "\033[92m{}\033[00m",
	"yellow": "\033[93m{}\033[00m",
	"yellow bold": "\033[1m\033[93m{}\033[00m",
	 "light purple":	"\033[94m{}\033[00m",
	"purple": "\033[95m{}\033[00m",
	"cyan": "\033[96m{}\033[00m",
	"cyan bold":"\033[1m\033[96m{}\033[00m",
	"light gray": "\033[97m{}\033[00m",
	"black": "\033[98m{}\033[00m"
}
indiList 		= []		#will hold all individuals
famList		= []		#will hold all families
indiLineInfo	={}
famLineInfo	={}




#---------------------### HELPER FUNCTIONS ###---------------------#
#Colors!!
def printColor(color, str, end="\n"):
	print(Colors[color].format(str), end=end)

#Given an id and an attribute of intrest, returns the value of the attribute desired ex lookup("birthday", "I343628")
def lookup(attr, id):
	for indi in indiList:			#loop over all individuals
		if id == indi['ID']:		#if we find id
			return indi[attr]			#return the individual's data that we desire

#Given an id,an attribute of intrest, and a list returns the value of the attribute desired ex lookup("birthday", "I343628", indiList)
def modified_lookup(attr, id, inputlist):
	for indi in inputlist:			#loop over all individuals
		if id == indi['ID']:		#if we find id
			return indi.get(attr, None)			#return the individual's data that we desire

#Calculate age difference fot get_parents_not_too_old() function
def get_age_difference(parent_age, child_age):
	age = parent_age - child_age
	return age

def getIndiLine(pid, tag):
	try:
		stri = str((indiLineInfo.get(pid)).get(tag))
	except:
		stri = ""
	return stri

def getFamLine(pid, tag):
	try:
		stri = str(famLineInfo[pid][tag])
	except:
		stri = ""
	return stri

#Return the difference of two dates in months
def diffMonth(d1, d2):
	if d1 is None or d2 is None:
		return None
	date1 = dateToCompare(d1)
	date2 = dateToCompare(d2)
	return (date1.year - date2.year) * 12 + date1.month - date2.month

#Calculate age given two dates. If death not supplied assume not dead
def calculateAge(born, death=False):
	if born is None:
		return 0
	born 	= datetime.strptime(born, "%d %b %Y")
	endDate 	= datetime.strptime(death, "%d %b %Y") if death else date.today() #if death is set, set end date as death. Otherwise, set end date as today
	return endDate.year - born.year - ((endDate.month, endDate.day) < (born.month, born.day))

#Returns true if date1 is before or equals date2,
def check_dateOrder(date1, date2):
	if (date1 is None):
		if(date2 is None):
			return True
		return False

	date1 = datetime.strptime(date1, "%d %b %Y")
	date2 = datetime.strptime(date2, "%d %b %Y") if date2 else None

	if date2 is None or date1 <= date2:
		return True
	else:
		return False

#Convert to datetime object
def dateToCompare(date):
	return datetime.strptime(date, "%d %b %Y")

#check age difference for a parent and a child
def get_age_difference(parent_age, child_age):
	try:
		return parent_age - child_age
	except:
		pass


#function to replace the children id(s) with their actual data
def replace_id_with_children_data(children_arr):
	new_arr = []
	for i in range(len(children_arr)):
		new_arr.append(look_for_child_by(children_arr[i]))
	return new_arr

# return all family ids to a record
def find_family_ids(fam_list):
	records = []
	for record in fam_list:
		records.append(record['ID'])
	return records

#return all married people to a record
def get_married_list(famList):
	fam_records = []
	fam_id_records = find_family_ids(famList)
	for id in fam_id_records:
		husband_name = modified_lookup('Husband Name', id, famList)
		wife_name = modified_lookup('Wife Name', id, famList)
		divorce_date = modified_lookup('Divorced', id, famList)
		if (divorce_date is None):
			fam_records.append([husband_name,wife_name])

	return fam_records


#---------------------### USER STORY FUNCTIONS ###---------------------#
#US12: Parents not too old | ND Sprint 1
#(father not 80 yrs older, and mother not 60 yrs older than child) ****start
#function to print father, mother and children data and display if parents are too hold to be a child's parent
def get_parents_not_too_old(famList):
	family = []
	table_arr = []
	father_age_limit = 80
	mother_age_limit = 60


	#loop to retrieve father, mother and children data from family record
	for i in range(len(famList)):
		#append specific data from famList to the family list
		family.append({'Husband_ID':famList[i]['Husband ID'], 'Wife_ID':famList[i]['Wife ID'],
			'Husband Name':famList[i]['Husband Name'], 'Wife Name':famList[i]['Wife Name'],
			'Husband Age': lookup('Age', famList[i]['Husband ID']), 'Wife Age': lookup('Age', famList[i]['Wife ID']),
			'Children': replace_id_with_children_data(famList[i]['Children'])})

	# loop to build list to hold father, mother and children data
	for j in range(len(family)):
		for k in range(len(family[j]['Children'])):
			#check to see if father is not 80 yrs older than children or if mother is not 60 yrs older than children
			father = 0 if family[j]['Husband Age'] is None else family[j]['Husband Age']
			mother = 0 if family[j]['Wife Age'] is None else family[j]['Wife Age']
			child = 0 if family[j]['Children'][k]['Age'] is None else family[j]['Children'][k]['Age']

			father_too_old = 'Yes' if get_age_difference(father, child) > father_age_limit else "No"
			mother_too_old = 'Yes' if get_age_difference(mother, child) > mother_age_limit else "No"

			#check to see if parents are older than children then if so append to table_arr
			if(father > child):
				table_arr.append([family[j]['Husband Name'],"Father", family[j]['Husband Age'],
					family[j]['Children'][k]['Name'], family[j]['Children'][k]['Gender'], family[j]['Children'][k]['Age'], father_too_old])
			if(mother > child):
				table_arr.append([family[j]['Wife Name'], "Mother", family[j]['Wife Age'],
					family[j]['Children'][k]['Name'], family[j]['Children'][k]['Gender'], family[j]['Children'][k]['Age'], mother_too_old])

	#bring list to a prettytable structure
	x = PrettyTable()
	x.field_names = ['Parent Name', 'Relationship', 'Parent Age', 'Child Name', 'Sex', 'Child Age', 'Parents too old']
	for n in range(len(table_arr)):
		x.add_row([table_arr[n][0], table_arr[n][1], table_arr[n][2],
			table_arr[n][3], table_arr[n][4], table_arr[n][5], table_arr[n][6]])


	print(x)
	return 1, x

	#************************************************************************end

#US20: Aunts and uncles | CC Sprint 3
# Aunts and uncles should not marry their nieces or nephews
def veifyNoAuntUncleMarrNieceNephew(indiList, famList):
	count = 0
	for family in famList:
		husbID		= family["Husband ID"]
		wifeID		= family["Wife ID"]
		husbGParents	= getGrandparents(husbID, indiList, famList)
		wifeGParents	= getGrandparents(wifeID, indiList, famList)
		husbParents	= getParents(husbID, indiList, famList)
		wifeParents	= getParents(wifeID, indiList, famList)

		auntMarriages	= set(husbGParents) & set(wifeParents)
		uncleMarriages	= set(wifeGParents) & set(husbParents)

		uncleMarriages.discard(None)
		auntMarriages.discard(None)

		if len(uncleMarriages) > 0: #if we have elements remaining in the intersection, this means an unlce married his niece
			count += 1
			printColor("yellow bold", "WARN: FAM: US20: {}: Uncle {} {} married his niece {} {}"\
				.format(family["ID"], husbID, family["Husband Name"], wifeID, family["Wife Name"]))

		if len(auntMarriages) > 0: #if we have elements remaining in the intersection, this means an aunt married her nephew
			count += 1
			printColor("yellow bold", "WARN: FAM: US20: {}: Aunt {} {} married hew nephew {} {}"\
				.format(family["ID"], wifeID, family["Wife Name"], husbID, family["Husband Name"]))

	if count == 0:
		printColor("green", "INFO: GEN: US20: No Aunts marrying their Nephews or Uncles marrying their Nieces")

	return count




#US21 | JT Sprint 2
# Checks the family list to ensure that all wives are female and all husbands are male
def check_gender_roles(famList):
	for family in famList:
		husbandGender = lookup("Gender" ,family["Husband ID"])
		wifeGender = lookup("Gender" ,family["Wife ID"])
		if husbandGender != "M":
			print("WARN: IND: US21: L{}: All husbands must be males".format(getIndiLine(family["Husband ID"], "SEX")))
			return False
		if wifeGender != "F":
			print("WARN: IND: US21: L{}: All wives must be female".format(getIndiLine(family["Wife ID"], "SEX")))
			return False
	print("INFO: GEN: US21: Gender roles are OK")
	return True

#US25 | JT Sprint 2
# Checks the family list to ensure that each family only has one child with the same name and birthday
def check_unique_child(famList):
	for family in famList:
		childrenList = {}
		for child in family["Children"]:
			name = lookup("Name", child)
			birthday = lookup("Birthday", child)
			if name in childrenList and birthday == childrenList[name]:
				print("WARN: FAM: US25: No more than one child with the same name and birth date should appear in a family")
				return False
			else:
				childrenList[name] = birthday
	print("INFO: GEN: US25: All Unique first names in families")
	return True

#US26: Corresponding entries | CC Sprint 3
#All family roles (spouse, child) specified in an individual record should have corresponding entries in the corresponding family records.
#Likewise, all individual roles (spouse, child) specified in family records should have corresponding entries in the corresponding  individual's records.
#I.e. the information in the individual and family records should be consistent.
def verifyCorrespondingEntries_ind(indiList, famList):
	count = 0
	for indi in indiList:
		indiID			= indi["ID"]
		childOfFamID		= indi.get("Child", None)
		spouseOfFamIDArray	= indi.get("Spouse", None)

		#now check that indiID appears in the child array of the family ID
		if (childOfFamID is not None) and (indiID not in modified_lookup("Children", childOfFamID, famList)):
			count += 1
			printColor("yellow bold", "WARN: FAM: US26: L{}: {}: {} {}'s individual record says they are a child in {}, but no corresponding family entry found"\
				.format(getIndiLine(indiID, "FAMC"), childOfFamID, indiID, indi["Name"], childOfFamID))

		for spouseOfFamID in spouseOfFamIDArray:
			if (spouseOfFamID is not None) and (indiID not in (modified_lookup("Husband ID", spouseOfFamID, famList), modified_lookup("Wife ID", spouseOfFamID, famList))):
				count += 1
				printColor("yellow bold", "WARN: FAM: US26: L{}: {}: {} {}'s individual record says they are a spouse in {}, but no corresponding family entry found"\
					.format(getIndiLine(indiID, "FAMC"), spouseOfFamID, indiID, indi["Name"], spouseOfFamID))

	return count

def verifyCorrespondingEntries_fam(indiList, famList):
	count = 0
	for fam in famList:
		famID			= fam["ID"]
		husbID			= fam["Husband ID"]
		wifeID			= fam["Wife ID"]
		childrenIDArray	= fam["Children"]

		husbFamilies = modified_lookup("Spouse", husbID, indiList)
		if husbID != "" and (husbFamilies is None or famID not in husbFamilies):
			count += 1
			printColor("yellow bold", "WARN: IND: US26: {}: family record {} has {} {} as husband, but his inividual record does not have corresponding spouse entry"\
				.format(husbID, famID, husbID, fam["Husband Name"]))

		wifeFamilies = modified_lookup("Spouse", wifeID, indiList)
		if wifeID != "" and (wifeFamilies is None or famID not in wifeFamilies):
			count += 1
			printColor("yellow bold", "WARN: IND: US26: {}: family record {} has {} {} as wife, but her inividual record does not have corresponding spouse entry"\
				.format(wifeID, famID, wifeID, fam["Wife Name"]))

		for childID in childrenIDArray:
			if famID != modified_lookup("Child", childID, indiList):
				count += 1
				printColor("yellow bold", "WARN: IND: US26: {}: family record {} has {} as child, but their inividual record does not have corresponding child entry"\
					.format(childID, famID, childID))

	return count

def verifyCorrespondingEntries(indiList, famList):
	return {
		"ind": verifyCorrespondingEntries_ind(indiList, famList),
		"fam": verifyCorrespondingEntries_fam(indiList, famList)
	}

#US29: Deceased list | ND Sprint 1
def get_deceased_records(indList):
	decease_list = []
	records = ""
	for record in indList:
		if (record['Alive'] == False):
			records = [record['ID'],record['Name'], record['Gender'], record['Birthday'], record['Age'],
			record['Death']]
			decease_list.append(records)

	#df = pd.DataFrame(decease_list, columns = ['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Death'])
	#print(df)
	return 1, decease_list
#***************************************************************************end


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

#Austin Luo
def marriageAge(indiList, famList):
	for family in famList:
		husbandID = family['Husband ID']
		wifeID = family['Wife ID']
		husbandBirthday = modified_lookup('Birthday', husbandID, indiList)
		wifeBirthday = modified_lookup('Birthday', wifeID, indiList)
		marriageDate = family['Married']
		husbandMarriageAge = calculateAge(husbandBirthday, marriageDate)
		wifeMarriageAge = calculateAge(wifeBirthday, marriageDate)
		if husbandMarriageAge < 14:
			print("WARN: IND: US10: " + husbandID + ": Husband married before 14 years old, married at " + str(husbandMarriageAge) + "yrs old")
		if wifeMarriageAge < 14:
			print("WARN: IND: US10: " + wifeID + ": Wife married before 14 years old, married at " + str(wifeMarriageAge) + "yrs old")

def realBirthday(indiList, famList):
	count = 0
	for family in famList:
		if 'Children' in family.keys():
			for childID in family["Children"]:
				childBirthday 	= modified_lookup("Birthday", childID, indiList)
				wifeDeath		= modified_lookup("Death", family['Wife ID'], indiList)
				husbDeath		= modified_lookup("Death", family['Husband ID'], indiList)
				if (check_dateOrder(childBirthday, wifeDeath) == False):
					print("ERRO: IND: US09: " + childID + ": Child was born on " + childBirthday + ", mother died on " + wifeDeath)
					count += 1
				monthDifference = diffMonth(husbDeath, childBirthday)
				if((monthDifference is not None) and monthDifference < -9):
					print("WARN: IND: US09: " + childID + ": Child was born on " + childBirthday + ", father died on " + husbDeath)
					count += 1
	return count

#US15 AL
def multipleSiblings(indiList, famList):
	for family in famList:
		if 'Children' in family.keys():
			if len(family['Children']) >= 15:
				print("WARN: FAM: US15: {} doesn't have less than 15 children".format(family["ID"]))
				return False

	print("INFO: FAM: US15: ALl families have fewer than 15 children")
	return True


#US14 AL
def multipleBirths(indiList, famList):
	for family in famList:
		if 'Children' in family.keys():
			if len(family["Children"]) > 5:
				birthdays =[]
				for childID in family["Children"]:
					birthdays.append(modified_lookup("Birthday", childID, indiList))

				birthdays = list(dict.fromkeys(birthdays))
				if len(birthdays) <= (len(family["Children"]) / 6):
					print("WARN: FAM: US14: More than 5 Children in {} were born on the same day".format(family["Children"]))
					return False

	print("INFO: FAM: US14: No more than 5 children born at the same time")
	return True

		# 	if len(famList[individual]['Children']) >= 5:
		# 		for firstchild in famList[individual]['Children']:
		# 			counter = 1
		# 			date = indiList[firstchild]['Birthday']
		# 			for secondchild in famList [individual]['Children']:
		# 				if(indiList[secondchild]['Birthday'] == date):
		# 					counter += 1
		# 				if(counter > 5):
		# 					return False
		# return True

def correctName(indiList):
	for individual in indiList:
		if 'Name'.isdigit():
			contains_digit = False
	return True



def largestName(famList):
	for family in famList:
		for famID in family:
			familyIdentification = modified_lookup('ID', famList)


"""
###########################
	for family in famList:
		childrenList = {}
		for child in family["Children"]:
			identification = lookup("ID", child)
			if identification > 5:
				print("No more than five children are allowed to be born at once.")
				return False
	print("All couples have five children or less.")
	return True
"""

def tooOld(indiList):
    for individual in indiList:
        individualAge = lookup("Age", individual)
        if individualAge > 130:
            print("No individuals allowed to be older 130 years old.")
            return False
    return True

# def multipleBirths(famList):
#     for family in famList:
#         childrenList = {}
#         childrenID = lookup("Children", family)
#         for children in family["Children"]:
#             print(childrenID)
#             return True
#     return False
#     print("This perseon does not have a child.")

#Checks date argument to see if that date is not after today's date
def validDate(arguments):
	current_date = date.today()
	try:
		date_arg = datetime.strptime(arguments, "%d %b %Y").date()
	except ValueError:
		raise ValueError("Incorrect data format, should be YYYY-MM-DD")

	if date_arg > current_date:
		return False
	return True

#function to find the children data
def getChildren_and_age(id):
	name = lookup('Name', id)
	age = lookup('Age', id)
	gender = lookup('Gender', id)
	birthday = lookup('Birthday', id)
	return {'Name': name, 'Age':age, 'Gender':gender, 'Birthday':birthday}

#function to replace the children id(s) with their actual data
def replace_id_with_children_data(children_arr):
	new_arr = []
	for i in range(len(children_arr)):
		new_arr.append(getChildren_and_age(children_arr[i]))
	return new_arr

#US03: Birth before death | CC Sprint 1:
#Verify that all death dates are after birth dates. Returns 0 if no offenders. If offenders detected, returns the number of them
def verifyBirthDeathDateOrder(indiList):
	for individual in indiList:
		if 'Child' in individual.keys():
			indiID = individual['ID']

			childBirthday = lookup("Birthday", indiID)
			childFamilyID = lookup("Child", indiID)

	warningList = []
	for indi in indiList:		#loop over all individuals
		if (check_dateOrder(indi.get('Birthday', None), indi.get('Death', None)) == False):	#using check_dateOrder, if Birthday is after Death append the offender to warningList
			warningList.append(indi)

	if len(warningList) < 1:		#if warningList is empty
		printColor("green", "INFO: GEN: US03: No Deaths before Births")
	else:
		def verifyBirthDeathDateOrderPrint(x):
			printColor("yellow bold", "ERRO: IND: US03: L{}: {}: {} died on {}, before their birthday of {}"\
				.format(getIndiLine(x['ID'], "DEAT"), x['ID'], x['Name'], x['Death'], x['Birthday']))
		pd.DataFrame(warningList).apply(lambda x: verifyBirthDeathDateOrderPrint(x), axis=1)

	return len(warningList)


#US04: Marriage before divorce | CC Sprint 1
#Verify that all divorce dates are after marriage dates. Returns 0 if no offenders. If offenders detected, returns the number of them
def verifyMarriageDivorceOrder(famList):
	warningList = []
	for f in famList:		#loop over all families
		if (check_dateOrder(f.get('Married', None), f.get('Divorced', None)) == False):	#using check_dateOrder, if Married is after Divorced append the offender to warningList
			warningList.append(f)

	if len(warningList) < 1:		#if warningList is empty
		printColor("green", "INFO: GEN: US04: No Divorces before Marriages")
	else:
		def verifyMarriageDivorceOrderPrint(x):
			printColor("yellow bold", "ERRO: FAM: US04: L{}: {}: {} and {} divorced on {}, before their marriage on {}"\
				.format(getFamLine(x['ID'], "DIV"), x['ID'], x['Husband Name'], x['Wife Name'], x['Divorced'], x['Married']))
		pd.DataFrame(warningList).apply(lambda x: verifyMarriageDivorceOrderPrint(x), axis=1)

	return len(warningList)

#US13 | SJ Sprint 1
#Sibling Spacing birth dates of siblings must be 8 months or more apart from each other or less than 2 days for twins
def SiblingSpacing(indiDF, famList, indiList):
	birthday = ''
	for fam in famList:

		childrenList = fam['Children']
		birthdays = list()
		for id in childrenList:
			birthday = modified_lookup("Birthday", id,indiList)
			birthdays.append(birthday)

		for index in range(0, len(birthdays) - 1):
			birthday_1 = birthdays[index]
			birthday_2 = birthdays[index + 1]
			date_1 = datetime.strptime(birthday_1, "%d %b %Y").date()
			date_2 = datetime.strptime(birthday_2, "%d %b %Y").date()
			# print("DEBUG")
			# print(date_1)
			# print(date_2)
			dayDifference = abs((date_1 - date_2).days)
			if dayDifference > 240 or dayDifference < 2:
				print('INFO: IND: US13: Day difference = ' + str(dayDifference))
			else:
				print('ERR: IND: US13: Siblings must be born at least 8 months apart or less than 2 days for twins')
				return False
	return True


#US16 | SJ Sprint 1
def maleLastNames(indiDF, famList):
	lastNamesEqual = False
	childrenName = ''	#init child / husb name and childrenID
	husbandName = ''
	childrenID = ''
	malesList = indiDF[(indiDF['Gender'] == 'M')] #created list of males
	for fam in famList:
		# print(fam)
		husbandName = fam['Husband Name'] #for each family stor the husb name
		lastName = re.findall("\/(.*)\/", str(husbandName))
		if len(lastName) > 0:
			lastName = lastName[0]
		else:
			lastName = ""
		childrenID = fam['Children'] #get the childrenid
		# print('children ids', str(childrenID))
		# print('husband Last name' , str(lastName))
		for id in childrenID: #for all ids in childrenID
			#print('\n', str(id))
			childFirstName = ""
			childLastName = ""
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

			if(lastName == childLastName or childLastName == ""): #if the childs name contains the husbands name its true otherwise false
				#print('Family name is ' + lastName)
				lastNamesEqual = True

			else:
				print("WARN: IND: US16: All male members of family should have same last name. Last name: {}. Child's name: {} {}".format(lastName, childFirstName, childLastName))
				return False
	return lastNamesEqual

#US13 SJ Sibling Spacing birth dates of siblings must be 8 months or more apart from each other or less than 2 days for twins
def SiblingSpacing(indiDF, famList):
	birthday = ''
	SiblingSpacing = True
	for fam in famList:
		i = 0
		childrenList = fam['Children']
		birthdays = list()
		for id in childrenList:
			birthday = lookup("Birthday", id)
			birthdays.append(birthday)
		#	print('birthday ' + str(birthdays))
		for index in range(0, len(birthdays)):
			birthday_1 = birthdays[index]
			for j in range(index + 1, len(birthdays)):
				birthday_2 = birthdays[j]
				date_1 = datetime.strptime(birthday_1, "%d %b %Y").date()
				date_2 = datetime.strptime(birthday_2, "%d %b %Y").date()
				dayDifference = abs((date_1 - date_2).days)
				if dayDifference > 240 or dayDifference < 2:
					print('INFO: IND: US13: Day difference = ' + str(dayDifference))
				else:
					print('ERR: IND: US13: Siblings must be born at least 8 months apart or less than 2 days for twins')
					return False

	return SiblingSpacing

#US19: First cousins should not marry | CC Sprint 2
#First cousins should not marry one another
def getParents(indiID, indiList, famList):
	familyID	= modified_lookup("Child", indiID, indiList)

	fatherID = modified_lookup("Husband ID", familyID, famList)
	motherID = modified_lookup("Wife ID", familyID, famList)

	return [fatherID, motherID]

def getGrandparents(indiID, indiList, famList):
	familyID = modified_lookup("Child", indiID, indiList)

	parentsID_arr = getParents(indiID, indiList, famList)
	grandParentsID_arr = []

	for parentID in parentsID_arr:
		grandParentsID_arr.extend(getParents(parentID, indiList, famList))

	return grandParentsID_arr
	# fatherID = modified_lookup("Husband ID", familyID, famList)
	# motherID = modified_lookup("Wife ID", familyID, famList)

	# fatherFamilyID = modified_lookup("Child", fatherID, indiList)
	# motherFamilyID = modified_lookup("Child", motherID, indiList)

	# fatherFatherID = modified_lookup("Husband ID", fatherFamilyID, famList)
	# fatherMotherID = modified_lookup("Wife ID", fatherFamilyID, famList)
	# motherFatherID = modified_lookup("Husband ID", motherFamilyID, famList)
	# motherMotherID = modified_lookup("Wife ID", motherFamilyID, famList)

	# return [fatherFatherID, fatherMotherID, motherFatherID, motherMotherID]

def verifyNoFirstCousinMarr(indiList, famList):
	warningList = []
	for family in famList:
		husbID		= family["Husband ID"]
		wifeID		= family["Wife ID"]
		husbGParents	= getGrandparents(husbID, indiList, famList)
		wifeGParents	= getGrandparents(wifeID, indiList, famList)

		for i in husbGParents:
			if i is not None and i in wifeGParents:
				warningList.append(family)
				break

	if len(warningList) < 1:
		printColor("green", "INFO: GEN: US19: No First Cousins married")
	else:
		printColor("yellow bold", "WARN: FAM: US19: First Cousins Marriages found:")
		print(pd.DataFrame(warningList), end="\n\n")

	return len(warningList)

# Sean James - US22 all IDs must be unique
def uniqueID(indiList):
	id_List = list()
	for i in range(len(indiList)):
		id = indiList[i]['ID']
		id_List.append(id)
	id_Set = set(id_List)
	unique_ids = len(id_Set) == len(id_List)

	return unique_ids

# Sean James US23 all names and Birthdates must be different
def uniqueNameAndBirthday(indiList):
	name_List = list()
	birthdate_List = list()
	for i in range(len(indiList)):
		name = indiList[i]['Name']
		name_List.append(name)
		birthdate = indiList[i]['Birthday']
		birthdate_List.append(birthdate)
	name_Set = set(name_List)
	birthdate_Set = set(birthdate_List)
	if (len(name_List) == len(name_Set)) and (len(birthdate_List) == len(birthdate_Set)):
		unique_NameAndBirthday = True
	else:
		unique_NameAndBirthday = False
	return unique_NameAndBirthday

# JW US07 - Checks age argument to ensure it is less than 150 years
def validAge(indiList):
	for person in indiList:
		age=person["Age"]
		if age >= 150:

			print("ERROR: INDIVIDUAL: US07: L" + getIndiLine(person["ID"], "BIRT") + " "  + str(person["ID"]) + ": More than 150 years old - Birth Date: " + str(person["Birthday"]))
			return False
	return True

#US02 | JT Sprint 1
def birthBeforeMarriage(famList):
	for family in famList:
		for childId in family["Children"]:
			marriageDate = dateToCompare(family['Married'])
			if childId != "NaN":
				birthday = dateToCompare(lookup("Birthday", childId))
				if marriageDate > birthday:
					return False
	return True


#US8 | JW Sprint 1
def birthBeforeMarriage2(famList, individualListName):
	for family in famList:
		for childId in family["Children"]:
			marriageDate = dateToCompare(family['Married'])
			if childId != "NaN":
				birthday = dateToCompare(modified_lookup("Birthday", childId, individualListName))
				if family.get("Divorced") != None:
					divorceDate = dateToCompare(family['Divorced'])
					divorceNineMonths = divorceDate + relativedelta(months=+9)
					if birthday > divorceNineMonths:
						print("ERROR: FAMILY: US46:", family["ID"] + ": Child " + str(childId) + " born " + str(birthday) + " after divorce on " + str(divorceDate))
						return False
				if marriageDate > birthday:
					print("ERROR: FAMILY: US46:", family["ID"] + ": Child " + str(childId) + " born " + str(birthday) + " before marriage on " + str(marriageDate))
					return False
	return True


#US11: No bigamy | CC Sprint 2:
#Marriage should not occur during marriage to another spouse
def getAnomaliesBigamy(remarriedSet, famDF, indiDF, maritalPosition):
	#Set up variables
	anomalyBigamyDF = pd.DataFrame()
	if maritalPosition == "Husband":
		maritalPositionID 	= "Husband ID"
		spousePositionID	= "Wife ID"
		spouseName		= "Wife Name"
	else:
		maritalPositionID 	= "Wife ID"
		spousePositionID	= "Husband ID"
		spouseName		= "Husband Name"

	#loop over every personID in the remarried Set
	for personID in remarriedSet:
		marrInfoDF = famDF.loc[		#Make a dataframe based on the famDF, but here all rows are related to personID
			(famDF[maritalPositionID] == personID),									#This line specifies the query
			['ID', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Married', 'Divorced']	#This line specifies what columns our output contains. Is independent from the above line
		]

		marrInfoDF.dropna(subset=['Husband Name', 'Wife Name'], inplace = True)
		print(marrInfoDF)
		#Merge data from indiDF into our newly created marrInfoDF table. We are intrested in getting Death dates from indiDF
		marrInfoDF = marrInfoDF.merge(indiDF[["ID", "Death"]], how="left", left_on=spousePositionID, right_on="ID")
		marrInfoDF.drop('ID_y', axis=1, inplace=True)							#drop the ID column as we dont need it
		marrInfoDF.rename(columns={"Death": "Spouse Death", "ID_x": "ID"}, inplace=True)		#Rename death to spouse death just to be more descriptive

		#Convert all dates to datetime so we can easily compare dates
		marrInfoDF['Married'] 		= pd.to_datetime(marrInfoDF['Married'], format='%d %b %Y', errors='coerce')
		marrInfoDF['Divorced'] 		= pd.to_datetime(marrInfoDF['Divorced'], format='%d %b %Y', errors='coerce')
		marrInfoDF['Spouse Death'] 	= pd.to_datetime(marrInfoDF['Spouse Death'], format='%d %b %Y', errors='coerce')

		#sort the table by Married, so we get the earliest marriage first
		marrInfoDF.sort_values(by=['Married'], inplace=True)
		marrInfoDF.reset_index(inplace=True, drop="Index")

		#Create four new columns that hold the previous row's info using .shift(), which copies Divorced, Spouse Death, Huband Name, and Husband ID from row 1 to row 2, from row 2 to row 3, etc.
		#This way when we look at one row, we also have information of the previous row in our own row.
		marrInfoDF[['prev_divorced', 'prev_spouseDeath', 'prev_spouseName', 'prev_spouseID']] = marrInfoDF[['Divorced', 'Spouse Death', spouseName, spousePositionID]].shift()

		#set the previous marriage end date to the previous divorce. If that doesnt exist, set it to the previous spouse's death date. if that didnt exist it will be NaT
		marrInfoDF['prev_marriageEndDate'] = np.where(pd.isnull(marrInfoDF['prev_divorced']), marrInfoDF['prev_spouseDeath'], marrInfoDF['prev_divorced'])
		marrInfoDF = marrInfoDF.iloc[1:]	#We don't care about the first row, because we can't tell if a bigamy is happening if we just have one entry for married

		#make a table for entries that have bigamy. This is the case when the Married date comes before the previous marriage's end date
		offendingEntriesDF = marrInfoDF.loc[
			~(marrInfoDF['Married'] > marrInfoDF['prev_marriageEndDate']) #~ means not. We have to do "not greater than" because any date < NaT returns false. But we want true so we flip
		]

		#Concatonate our findings to a table that has all bigamies
		anomalyBigamyDF = pd.concat([anomalyBigamyDF, offendingEntriesDF])

	return anomalyBigamyDF

#returns the number of offenders who commit bigamy. Prints any offenders.
def verifyBigamy(famList, famDF, indiDF):
	husbID_list 		= famDF["Husband ID"].to_list()	#list of all husband IDs, duplicates included
	wifeID_list 		= famDF["Wife ID"].to_list()
	remarriedSet_male 	= set([])
	remarriedSet_female = set([])

	#identify all posssible cases
	for families in famList:					#loop through all families
		husbID = families["Husband ID"]			#grab this row's husband ID
		wifeID = families["Wife ID"]

		if(husbID_list.count(husbID) > 1):			#Check if this row's husb ID appears more than once in the husbID list
			remarriedSet_male.add(husbID)

		if(wifeID_list.count(wifeID) > 1):			#Check if this row's wife ID appears more than once in the wifeID list
			remarriedSet_female.add(wifeID)

	maleBigamyDF	= getAnomaliesBigamy(remarriedSet_male, famDF, indiDF, "Husband")
	femaleBigamyDF	= getAnomaliesBigamy(remarriedSet_female, famDF, indiDF, "Wife")

	numOffenders = len(maleBigamyDF) + len(femaleBigamyDF)
	if numOffenders > 0:	#Print offending entries if either dataframe has entries
		def maleBigamyPrint(x):
			printColor("yellow bold", "WARN: FAM: US11: {}: Husband {} married {} on {}, but he was still married to {}"\
				.format(x["ID"], x["Husband Name"], x["Wife Name"], x["Married"].date(), x["prev_spouseName"]), end="")
			if pd.isnull(x['prev_marriageEndDate']):
				printColor("yellow bold", ".")
			else:
				printColor("yellow bold", " until {}.".format(x["prev_marriageEndDate"].date()))

		def femaleBigamyPrint(x):
			printColor("yellow bold", "WARN: FAM: US11: {}: Wife {} married {} on {}, but she was still married to {}"\
				.format(x["ID"], x["Wife Name"], x["Husband Name"], x["Married"].date(), x["prev_spouseName"]), end="")
			if pd.isnull(x['prev_marriageEndDate']):
				printColor("yellow bold", ".")
			else:
				printColor("yellow bold", " until {}.".format(x["prev_marriageEndDate"].date()))

		maleBigamyDF.apply(lambda x: maleBigamyPrint(x), axis=1)
		femaleBigamyDF.apply(lambda x: femaleBigamyPrint(x), axis=1)
	else:
		printColor("green", "INFO: GEN: US11: No Bigamy")

	return numOffenders

#US44: Grandparents | CC Sprint 4
#Grandparents should not marry their grandchildren
def verifyNoGrandparentMarrGranchild(indiList, famList):
	count = 0
	for family in famList:
		husbID		= family["Husband ID"]
		wifeID		= family["Wife ID"]
		husbGParents	= getGrandparents(husbID, indiList, famList)
		wifeGParents	= getGrandparents(wifeID, indiList, famList)

		if husbID in wifeGParents:
			count += 1
			printColor("yellow bold", "WARN: FAM: US44: {}: Grandpa {} {} married his granddaughter {} {}"\
				.format(family["ID"], husbID, family["Husband Name"], wifeID, family["Wife Name"]))

		if wifeID in husbGParents:
			count += 1
			printColor("yellow bold", "WARN: FAM: US44: {}: Grandma {} {} married her grandson {} {}"\
				.format(family["ID"], wifeID, family["Wife Name"], husbID, family["Husband Name"]))


	if count == 0:
		printColor("green", "INFO: GEN: US44: No Grandparents marrying their Grandchildren")

	return count


#US45 JW - Siblings < 35 year age difference
def siblingAgeDiff(famList, individualListName):
	for family in famList:
		if len(family["Children"]) > 1:
			dlow = dateToCompare(modified_lookup("Birthday", family["Children"][0],individualListName))
			dhigh = dateToCompare(modified_lookup("Birthday", family["Children"][0], individualListName))
			lowid=family["Children"][0]
			highid=birthday=family["Children"][0]
			for childId in family["Children"]:
				birthday = dateToCompare(modified_lookup("Birthday", childId, individualListName))
				if birthday < dlow:
					dlow=birthday
					lowid=childId
				if birthday > dhigh:
					dhigh=birthday
					highid=childId
			ageDiff = dhigh.year - dlow.year - ((dhigh.month, dhigh.day) < (dlow.month, dlow.day))
			if ageDiff >= 35:
				print("ERROR: FAMILY: US45:", family["ID"] + ": Age difference between older sibling (" + str(lowid) + ") and younger sibling ("+  str(highid)+ ") is", ageDiff, "which is not less than 35 years")
				return False
	return True

#US46 JW - Children>15 yr age difference parents
def childParentAgeDiff(famList, individualListName):
	for family in famList:
		dhus = dateToCompare(modified_lookup("Birthday", family["Husband ID"],individualListName))
		dwife = dateToCompare(modified_lookup("Birthday", family["Wife ID"], individualListName))
		dlow = dhus
		parid = family["Husband ID"]
		if dwife > dhus:
			parid = family["Wife ID"]
			dlow = dwife
		for childId in family["Children"]:
			birthday = dateToCompare(modified_lookup("Birthday", childId, individualListName))
			ageDiff = birthday.year - dlow.year - ((birthday.month, birthday.day) < (dlow.month, dlow.day))
			if ageDiff <= 15:
				print("ERROR: FAMILY: US46:", family["ID"] + ": Age difference between child (" + str(childId) + ") and parent ("+  str(parid)+ ") is", ageDiff, "which is not more than 15 years")
				return False
	return True

#US51 JW - List family with most members
def largestFamily(famList):
	if(len(famList)==0): return "N/A"
	largest_size = 0
	largest_id = ""
	for family in famList:
		size=2+len(family["Children"])
		if(size>largest_size):
			largest_size=size
			largest_id = family["ID"]
	print("STATS: FAMILY: US51: The largest family is " + str(largest_id) + " with size " + str(largest_size) + " (living or deceased)")
	return largest_id

# US24 Unique families by spouses
def check_dupe_spouses(famList):
	spouse_list = []
	for family in famList:
		try:
			marriage_date = family["Married"]
			husband = family["Husband Name"]
			wife = family["Wife Name"]
			entry = marriage_date + "_" + husband + "_" + wife
			spouse_list.append(entry)
		except:
			pass
	if len(set(spouse_list)) != len(spouse_list):
		print("ERROR: US 24: No more than one family with the same spouses by name and the same marriage date should appear in a GEDCOM file")
		return False
	return True

#US27- Include individual ages
def get_individual_age(indList):
	records = []
	for person in indList:
		records.append([person['Name'], person['Age']])
	print('US27 - Include individual ages')
	df = pd.DataFrame(records, columns = ['Name','Age'])
	print(df)
	return records

#US30 List living married
def get_living_married(ind_list, famList):
	living_marriage = []
	all_deceased_names = []
	marriage_records = get_married_list(famList)
	deceased = get_deceased_records(ind_list)[1]
	for j in range(len(deceased)):
		all_deceased_names.append(deceased[j][1])

	for k in range(len(marriage_records)):
		ind_record = marriage_records[k]
		result = any(elem in ind_record  for elem in all_deceased_names)
		if result:
			k += 1
		else:
			living_marriage.append(ind_record)
	print('US30 - List living married')
	df = pd.DataFrame(living_marriage, columns = ['Husband Name','Wife Name'])
	print(df)
	return living_marriage


#JW- US31 List living Single
def get_living_single(ind_list, famList):
	all_bad_ids = []
	deceased = get_deceased_records(ind_list)[1]
	for j in range(len(deceased)):
		all_bad_ids.append(deceased[j][0])
	for family in famList:
		all_bad_ids.append(family['Husband ID'])
		all_bad_ids.append(family['Wife ID'])
	all_good_ids = []
	add_person = True
	for person in ind_list:
		add_person = True
		for id in all_bad_ids:
			if (id == person['ID']):
				add_person = False
		if (add_person == True):
			all_good_ids.append(person['Name'])
	print('US31 - List living single')
	df = pd.DataFrame(all_good_ids, columns = ['Living Single'])
	print(df)
	return all_good_ids

#JW- US48 List children with same birthdays
def get_children_same_birthdays(ind_list, famList):
	same_birthdays = []
	for family in famList:
		used_set = set()
		children = family["Children"]
		for i in range(0, len(children)):
			if children[i] in used_set:
				continue
			used_list = []
			used_list.append(children[i])
			birthday_1 = modified_lookup("Birthday", children[i], ind_list)
			for j in range(i + 1, len(children)):
				if children[j] in used_set:
					continue
				birthday_2 = modified_lookup("Birthday", children[j], ind_list)
				if (birthday_2 == birthday_1):
					used_list.append(children[j])
			if len(used_list) > 1:
				same_birthdays.append(used_list)
				for child in used_list:
					used_set.add(child)
	print('US48 - List children with same birthdays\n', same_birthdays)
	return same_birthdays


#JW- US52 List children named after their parent
def get_children_named_after_parent(ind_list, famList):
	named_after = []
	for family in famList:
		husband = family["Husband Name"]
		wife = family["Wife Name"]
		children = family["Children"]
		for child in children:
			child_name = modified_lookup("Name", child, ind_list)
			if (child_name == husband) or (child_name == wife):
				named_after.append(child)
	print('US52 - List children named after parent\n', named_after)
	return named_after


#JW- US34 Large Age Differences
def get_large_age_diff(ind_list, famList):
	large_age_list = []
	for family in famList:
		try:
			dhus = dateToCompare(modified_lookup("Birthday", family["Husband ID"],ind_list))
			dwife = dateToCompare(modified_lookup("Birthday", family["Wife ID"], ind_list))
			dmarr = dateToCompare(family['Married'])
			husAge = dmarr.year - dhus.year - ((dmarr.month, dmarr.day) < (dhus.month, dhus.day))
			wifeAge = dmarr.year - dwife.year - ((dmarr.month, dmarr.day) < (dwife.month, dwife.day))
			agehigh = husAge
			agelo = wifeAge
			if (wifeAge > husAge):
				agehigh = wifeAge
				agelo = husAge
			if (agehigh > (agelo*2)):
				large_age_list.append([family['Husband Name'], family['Wife Name']])
		except:
			pass
	df = pd.DataFrame(large_age_list, columns = ['Husband Name', 'Wife Name'])
	if len(df) < 1:
		print('US34 - No large age differences to list')
	else:
		print('US34 - List large age differences')
		print(df)
	return large_age_list


#US 35 SJ List recent births, the last 30 days
def listRecentBirths(indiList):
	recentBirthdays = list()
	today = date.today()
	y = today - timedelta(days=30)
	for i in indiList:
		x = i['Birthday']
		birthday = datetime.strptime(x, "%d %b %Y").date()
		if(birthday > y):
			recentBirthdays.append(i['Name'])
		else:
			pass
	if not recentBirthdays:
		print("There have been no recent birthdays")
		return False
	else:
		print("The recent birthdays are: " + str(recentBirthdays))
		return True

#US 36 ND List recent deaths
def findRecentDeath(indiList):
	recent_death_list = []
	today_date = date.today()
	thirty_days_ago = today_date - timedelta(days=30)
	epoch_time = "1 JAN 1970"
	formal_epoch_time = datetime.strptime(epoch_time, "%d %b %Y").date()
	for people in indiList:
		validate_death_date = people.get('Death', formal_epoch_time)
		if validate_death_date == formal_epoch_time:
			continue
		else:
			formal_death_date = datetime.strptime(validate_death_date, "%d %b %Y").date()
			if (formal_death_date>thirty_days_ago and formal_death_date<today_date):
				recent_death_list.append([people['Name'], people['Death']])
	if(len(recent_death_list) <=0):
		print('There are no death in the last 30 days')
		return False
	else:
		print('List of people who died in the last 30 days:')
		df = pd.DataFrame(recent_death_list, columns = ['Name', 'Death'])
		print(df)
		return True


#US 38 SJ List upcoming, the next 30 days
def listUpcomingBirthdays(indiList):
	upcomingBirthdays = list()
	today = date.today()
	y = today + timedelta(days=30)
	for i in indiList:
		x = i['Birthday']
		birthday = datetime.strptime(x, "%d %b %Y").date()
		if(today < birthday < y):
			upcomingBirthdays.append(i['Name'])
		else:
			pass
	if not upcomingBirthdays:
		print("There are no coming birthdays")
		return False
	else:
		print("The next birthdays are: " + str(upcomingBirthdays))
		return True

#US 42 Reject Illegitimate Dates
def isDateLegitimate(date):
	month_dates = {
		"JAN": 31,
		"FEB": 28,
		"MAR": 31,
		"APR": 30,
		"MAY": 31,
		"JUN": 30,
		"JUL": 31,
		"AUG": 31,
		"SEP": 30,
		"OCT": 31,
		"NOV": 30,
		"DEC": 31,
	}
	date_split = date.split(" ")
	day = int(date_split[0])
	month = date_split[1]
	if month_dates[month] < day:
		return False
	return True


#US 43 ND Born Before Parents
def FindChildrenBornBeforeParent(famList):
	family = []
	children_and_parent_data = []
	zero = 0

	#loop to retrieve father, mother and children data from family record
	for i in range(len(famList)):
		#append specific data from famList to the family list
		family.append({'Husband_ID':famList[i]['Husband ID'],
			'Wife_ID':famList[i]['Wife ID'],
			'Husband Name':famList[i]['Husband Name'],
			'Wife Name':famList[i]['Wife Name'],
			'Husband Birthday': lookup('Birthday', famList[i]['Husband ID']),
			'Wife Birthday': lookup('Birthday', famList[i]['Wife ID']),
			'Husband Age': lookup('Age', famList[i]['Husband ID']),
			'Wife Age': lookup('Age', famList[i]['Wife ID']),
			'Children': replace_id_with_children_data(famList[i]['Children'])})

	# loop to build list to hold father, mother and children data
	for j in range(len(family)):
		for k in range(len(family[j]['Children'])):
			#check to see if children are not born before or on the same date as their father
			if check_dateOrder(family[j]['Children'][k]['Birthday'],family[j]['Husband Birthday'] ):
				children_and_parent_data.append([family[j]['Husband Name'],family[j]['Husband Age'],
					family[j]['Children'][k]['Name'],family[j]['Children'][k]['Age'] ])
				print("WARN: IND: US43: " + family[j]['Children'][k]['Name'] + " was born on (" + family[j]['Children'][k]['Birthday']
					+  ") the same date or before his/her father " + family[j]['Husband Name'] + " who were born on (" + family[j]['Husband Birthday'] + ").")

			#check to see if children are not born before or on the same date as their mother
			if check_dateOrder(family[j]['Children'][k]['Birthday'],family[j]['Wife Birthday'] ):
				children_and_parent_data.append([family[j]['Wife Name'],family[j]['Wife Age'],
					family[j]['Children'][k]['Name'],family[j]['Children'][k]['Age'] ])
				print("WARN: IND: US43: " + family[j]['Children'][k]['Name'] + " was born on (" + family[j]['Children'][k]['Birthday']
					+  ") the same date or before his/her mother " + family[j]['Wife Name'] + " who were born on (" + family[j]['Wife Birthday'] + ").")

	if len(children_and_parent_data)<=0:
		print('There are no children born before or on the same date as parent')
		return False
	else:
		return True

#US39 SJ Upcoming anniversaries
#marrige in the next 30 days
def upcomingAnni(famList):
	#get the marrige dates for couples
	#check if the month and date is coming up
	upcomingMarr = list()
	today = date.today()
	y = today + timedelta(days=30)
	for i in famList:
		x = i['Married']
		marrDate = datetime.strptime(x, "%d %b %Y").date()
		if(today < marrDate < y):
			upcomingMarr.append(i['Husband Name'])
		else:
			pass
	if not upcomingMarr:
		print("There are no upcoming marriges")
		return False
	else:
		print("The next marriges are: " + str(upcomingMarr))
		return True

#US53 Same name | CC Sprint 4
#List individuals who share the same name
def sameName(indiDF):
	count = 0
	names	= indiDF["Name"].tolist()
	ids		= indiDF["ID"].tolist()

	nameIDDict = {}

	for i in range(len(names)):
		name = names[i]
		j = i+1
		while j < len(names):
			if names[j] == name:
				if name not in nameIDDict:
					nameIDDict[name] = [ids[i], ids[j]]
				else:
					nameIDDict[name].append(ids[j])
					nameIDDict[name] = list(dict.fromkeys(nameIDDict[name]))
			j+=1

	for k in nameIDDict:
		count += 1
		printColor("black", "INFO: IND: US53: The following IDs share the same name {}: {}"\
				.format(k, nameIDDict[k]))

	return count

#US55 List recent dead divorcies
def listDeceasedDivor(indiDF, famList):
	divorcedL = list()
	deceasedL = list()
	for i in famList:
		if i.get("Divorced") != None:
			divorcedL.append(i['Husband Name'])
			divorcedL.append(i['Wife Name'])

	for i in divorcedL:

		person = indiDF[(indiDF['Name'] == i)]
		death = str(person.loc[person['Name'] == i, ['Death']])
		if 'NaN' in death:
			pass

		else:
			deceasedL.append(i)

	if not deceasedL:
		print('There are no deceased divorced members')
		return False
	else:
		print('Deceased list of divorced members is ' + str(deceasedL))
		return True


#US 57 list living widowed
def get_list_of_widow(indList, famList):
	print('US 57: list of living widows')
	divorced_list = {}
	no_both_couples_died_list = []
	no_divorced_array = []
	decease_array = []
	all_individuals_alive = []
	no_both_couples_alive = []
	marriage_with_widowed = []
	living_couples = []

	#get individuals ids who died
	decease_list = get_deceased_records(indList)[1]
	for i in range(len(decease_list)):
		decease_array.append(decease_list[i][0])

	#get all individual ids who are alive
	for indi_record in indList:
		if indi_record['Alive'] == True:
			all_individuals_alive.append(indi_record['ID'])

	#get all ids of marriage with divorce
	for divorced in famList:
		formal_divorce = divorced.get('Divorced')
		if formal_divorce != None:
			divorced_list[divorced['ID']] = formal_divorce

	family_ids_of_divorcees = divorced_list.keys()

	#get family marriage that does not have any divorce
	for a_record in famList:
		if a_record['ID'] not in family_ids_of_divorcees:
			no_divorced_array.append(a_record)

	# get marriage where both couples are not dead
	for marriage_record in no_divorced_array:
		husband_ids = marriage_record.get('Husband ID')
		wife_ids = marriage_record.get('Wife ID')
		if husband_ids not in decease_array or wife_ids not in decease_array:
			no_both_couples_died_list.append(marriage_record)

	#get marriage where one spouse died
	for m_record in no_both_couples_died_list:
		husband_ids = m_record.get('Husband ID')
		wife_ids = m_record.get('Wife ID')
		if husband_ids not in all_individuals_alive and wife_ids in all_individuals_alive:
			marriage_with_widowed.append(m_record)
		elif wife_ids not in all_individuals_alive and husband_ids in all_individuals_alive:
			marriage_with_widowed.append(m_record)

	#get marriage records where both couples are alive
	for alive_record in no_both_couples_died_list:
		husband_ids = alive_record.get('Husband ID')
		wife_ids = alive_record.get('Wife ID')
		if husband_ids in all_individuals_alive and wife_ids in all_individuals_alive:
			living_couples.append(alive_record)

	#get ids for all living couples
	living_couples_ids=[]
	for c_record in living_couples:
		living_couples_ids.append(c_record['Husband ID'])
		living_couples_ids.append(c_record['Wife ID'])

	#remove duplicate living couple ids
	formal_living_couples_ids = list(set(living_couples_ids))

	#get ids of marriage with widows that are alive
	widow_marriage_ids = []
	for widow_marriage in marriage_with_widowed:
		valid_husband_death = modified_lookup('Death',widow_marriage['Husband ID'], indList)
		valid_wife_death = modified_lookup('Death',widow_marriage['Wife ID'], indList)
		if valid_husband_death == None:
			widow_marriage_ids.append(widow_marriage['Husband ID'])
		if valid_wife_death == None:
			widow_marriage_ids.append(widow_marriage['Wife ID'])

	#check to see if widow is currently married and if not add to list
	widow_ids = []
	for w_record in widow_marriage_ids:
		if w_record not in formal_living_couples_ids:
			widow_ids.append(w_record)

	#return name of living widows
	living_widow_list = []
	for p_id in widow_ids:
		living_widow_list.append(modified_lookup('Name', p_id, indList))

	if(len(living_widow_list)<=0):
		print('No living widow')
		return False
	else:
		print(living_widow_list)
		return True


#US61 list of oldest in family
#helper method to locate if one parent or both parents are alive
def check_if_parents_alive(indList, famList):
	#retrieve ids all the person who died
	decease_array = []
	family_obj = {}
	deceased_data = get_deceased_records(indList)[1]
	for dead_person in deceased_data:
		decease_array.append(dead_person[0])

	#check if at least one parent is alive or both
	for fam_record in famList:
		husband_id = fam_record.get('Husband ID')
		wife_id = fam_record.get('Wife ID')
		if(husband_id in decease_array and wife_id in decease_array):
			family_obj[fam_record['ID']] = []
		if husband_id in decease_array and wife_id not in decease_array:
			family_obj[fam_record['ID']] = [wife_id]
		if husband_id not in decease_array and wife_id in decease_array:
			family_obj[fam_record['ID']] = [husband_id]
		if(husband_id not in decease_array and wife_id not in decease_array):
			family_obj[fam_record['ID']] = [husband_id, wife_id]
	return family_obj

def get_list_of_oldest(ind, fam):
	print('US 61: list of oldest in family')
	oldest_list = []
	children_alive = {}

	#get marriage where at least there is one parent or both alive or no parent is alive
	data = check_if_parents_alive(ind, fam)

	#loop to see who is the oldest parent in family if at least one is alive
	#or who is the oldest child if no parent are live
	#or if everyone in the family died including parents and children
	for key in data:
		data_id = data[key]
		lengthy_key = len(data_id)

		#if there is no parent alive, go to children hierarchy in family
		if lengthy_key < 1:

			#list of ids of deceased person
			decease_array = []
			deceased_data = get_deceased_records(ind)[1]
			for dead_person in deceased_data:
				decease_array.append(dead_person[0])

			#when there is no parent alive, loop to find all children alive in their respective family
			for marr in fam:
				fam_id = marr['ID']
				if key == fam_id:
					children_data = marr['Children']

					#remove children that are not alive
					alive_arr = []
					for ind_kid in children_data:
						if ind_kid not in decease_array:
							alive_arr.append(ind_kid)
					children_count = len(alive_arr)

					#if no parent or children is alive in family
					if(children_count<1):
						print('No one is alive in family' + " " + key)

					#if at least a child is alive, add to children_alive
					else:
						group_children = []
						for child in alive_arr:
							group_children.append(child)
						children_alive[fam_id] = group_children

			#check which child is oldest and get their ids
			for ind_child in children_alive:
				children_arr = children_alive[ind_child]

				#if there is only one child alive in family
				if(len(children_arr)== 1):
					oldest_list.append([ind_child, children_arr[0]])

				#if there is more than 1 child alive
				else:
					children_ages = {}
					for i in range(len(children_arr)):
						children_ages[children_arr[i]] = modified_lookup('Age', children_arr[i], ind)

					#get the id of person who is oldest when there are more than 1 child alive in family
					child_id = max(children_ages.items(), key=operator.itemgetter(1))[0]
					oldest_list.append([ind_child, child_id])


		#if parent or parents are  alive, go to parent hierarchy, check who is the oldest
		else:
			#if both parents are alive
			if(lengthy_key>1):
				first_person_age = modified_lookup('Age', data_id[0], ind)
				second_person_age = modified_lookup('Age', data_id[1], ind)

				if(first_person_age>second_person_age):
					oldest_list.append([key, data_id[0]])
				else:
					oldest_list.append([key, data_id[1]])

			#if only one parent is alive
			else:
				individual_id = data_id[0]
				oldest_list.append([key, individual_id])

	#remove duplicate arrays
	modified_oldest_list = np.unique(oldest_list,axis=0)

	#now replace ids with name of person the id belong to
	message = [[item[0], modified_lookup('Name', item[1], ind)] for item in modified_oldest_list]

	#print names of person who is the oldest in their respective family
	for data in message:
		print(str(data[1]) + ' is the oldest in family ' + str(data[0]))
	if(len(modified_oldest_list)<=0):
		return False
	else:
		return True


#---------------------### CORE FUNCTIONS ###---------------------#
#Given a gedcom file, returns indi and fam tables, and also returns indi and fam lists.
def generateInitialData(fileName):
	# global indiDF, indiList, famDF, famList
	with open(fileName, "r", encoding="utf-8") as inFile:		#open the file provided in the argument
		line_num = 0
		skipNextLines = False #boolean flag for if we should read the next lines following a tag lvl 0 or not
		currentID		= None

		for line in inFile:
			line_num		+= 1
			level		= ""
			tag			= ""
			valid		= ""
			arguments		= ""
			tokenizedStr	= re.search("(\d) (\S*) ?(.*)", line).groups()			#Use regex to store each token into a var. "1 NAME Bob /Smith/" becomes ["1", "NAME", "Bob /Smith/"]

			level		= tokenizedStr[0]

			#Check if third token is in the special list
			if tokenizedStr[2] in THIRD_TOKEN_TAGS or level == "0":
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
					print("ERRO: GEN: US01: L" + str(line_num) + ": No dates should be after the current date. Received: "+ arguments)
				if not isDateLegitimate(arguments):
					print("ERRO: GEN: US42: L" + str(line_num) + ": Date does not match month. Received: "+ arguments)



			if level == '0':
				if tag == "INDI":
					try:
						indiList[len(indiList) - 1] = newestIndiv
					except:
						pass
					newIndiv 			= {}
					newIndiv['ID'] 	= arguments
					newIndiv['Alive'] 	= True
					newIndiv['Spouse']	= []
					indiList.append(newIndiv)
					skipNextLines 		= False
					if currentID is None:
						currentID = arguments
						indiLineInfo[currentID] = {}
						indiLineInfo[currentID]["Start"] = line_num
					else:
						indiLineInfo[currentID]["End"] = line_num - 1
						currentID = arguments
						if currentID not in indiLineInfo:
							indiLineInfo[currentID] = {}
						indiLineInfo[currentID]["Start"] = line_num
				elif tag == "FAM":
					newFam 			= {}
					newFam['ID'] 		= arguments
					newFam['Children']	= []
					newFam['Husband ID']	= ""
					newFam['Wife ID']		= ""
					famList.append(newFam)
					skipNextLines		= False
				elif tag == "SUBM":
					skipNextLines		= True


			elif skipNextLines == False and level == '1':
				nextLineBirt 	= False
				nextLineDeat 	= False
				nextLineMarr 	= False
				nextLineDiv 	= False
				newestIndiv 	= indiList[-1] if indiList else None	#This syntax chooses the the last element in indiList if it exists, otherwise the newestIndiv is None
				newestFam		= famList[-1] if famList else None
				if tag == "NAME":
					newestIndiv['Name'] 			= arguments
					indiLineInfo[currentID]["NAME"]	= line_num
				elif tag == "SEX":
					newestIndiv['Gender'] 			= arguments
					indiLineInfo[currentID]["SEX"]	= line_num
				elif tag == "BIRT":
					nextLineBirt 					= True
					indiLineInfo[currentID]["BIRT"]	= line_num + 1
				elif tag == "DEAT":
					nextLineDeat 					= True
					indiLineInfo[currentID]["DEAT"]	= line_num + 1
				elif tag == "MARR":
					nextLineMarr 					= True
					indiLineInfo[currentID]["MARR"]	= line_num + 1
				elif tag == "DIV":
					nextLineDiv					= True
					indiLineInfo[currentID]["DIV"]	= line_num + 1
				elif tag == "FAMS":
					newestIndiv['Spouse'].append(arguments)
					indiLineInfo[currentID]["FAMS"]	= line_num
				elif tag == "FAMC":
					newestIndiv['Child'] 			= arguments
					indiLineInfo[currentID]["FAMC"]	= line_num
				elif tag == "HUSB":
					newestFam['Husband ID'] 			= arguments
					indiLineInfo[currentID]["HUSB"]	= line_num
				elif tag == "WIFE":
					newestFam['Wife ID'] 			= arguments
					indiLineInfo[currentID]["WIFE"]	= line_num
				elif tag == "CHIL":
					newestFam['Children'].append(arguments)
					indiLineInfo[currentID]["CHIL"]	= line_num


			elif skipNextLines == False and level == '2':
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
			"famList":	famList,
			"indiLineInfo":indiLineInfo,
			"famLineInfo":	famLineInfo
		}

#Reset global variables
def reset():
	global indiList, famList
	indiDF = []
	indiList = []
	famDF = []
	famList = []

def findTwins(famList):
	twins = []
	for family in famList:
		children = family["Children"]
		for i in range(0, len(children)):
			birthday1 = lookup("Birthday", children[i])
			for j in range(i + 1, len(children)):
				birthday2 = lookup("Birthday", children[j])
				if birthday1 == birthday2:
					twins.append([children[i], children[j]])
	print("Twins are:", twins)
	return twins

def findTriplets(famList):
	triplets = []
	for family in famList:
		children = family["Children"]
		for i in range(0, len(children)):
			birthday_1 = lookup("Birthday", children[i])
			for j in range(i + 1, len(children)):
				birthday_2 = lookup("Birthday", children[j])
				for k in range(j + 1, len(children)):
					birthday_3 = lookup("Birthday", children[k])
					if birthday_1 == birthday_2 == birthday_3:
						triplets.append([children[i], children[j], children[k]])
	print("triplets are:", triplets)
	return triplets


#---------------------### MAIN CODE ###---------------------#
def main():
	if(len(sys.argv) != 2):	#if we don't have 2 arguments,
		printColor("red bold","ERRO: Please provide a GEDCOM file.\nUSAGE: python3 script.py path/to/file.ged")
	else:
		gedcomStructuredData = generateInitialData(sys.argv[1]) #store the tables and lists into gedcomStructuredData

		indiDF		= gedcomStructuredData['indiDF']
		famDF		= gedcomStructuredData['famDF']
		indiList		= gedcomStructuredData['indiList']
		famList		= gedcomStructuredData['famList']
		indiLineInfo	= gedcomStructuredData['indiLineInfo']
		famLineInfo	= gedcomStructuredData['famLineInfo']

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

		def printIndi():
			printColor("cyan bold", "Individuals")
			print(indiDF, end="\n\n")
		def printFam():
			printColor("cyan bold","Families")
			print(famDF, end="\n\n")
		printIndi()
		printFam()
		indiDF.to_csv('indi.csv')
		famDF.to_csv('fam.csv')

		# vvv BEGIN USER STORY CALLS BELOW vvv

		#US02
		if not birthBeforeMarriage(famList):
			print("WARN: IND: US02: All children must be born after marriage")

		#US03
		verifyBirthDeathDateOrder(indiList)

		#US04
		verifyMarriageDivorceOrder(famList)

		#US07
		validAge(indiList)

		#US08
		birthBeforeMarriage2(famList, indiList)

		#Qualified
		print(print_data(indiList))

		#US09
		realBirthday(indiList, famList)

		#US10
		marriageAge(indiList, famList)

		#US11
		verifyBigamy(famList, famDF, indiDF)

		#US12
		get_parents_not_too_old(famList)

		#US14
		multipleBirths(indiList, famList)

		#US15
		multipleSiblings(indiList, famList)

		#US16
		if(maleLastNames(indiDF, famList)):
			printColor('green', 'INFO: GEN: US16: All males have same last name')
		else:
			print("\n")
			print('All males do not have the same last name')
			print("\n")
		#US13
		if SiblingSpacing(indiDF,famList) == False:
			print('Siblings are too close together and they are not twins check birth dates')
		else:
			pass

		#US19
		verifyNoFirstCousinMarr(indiList, famList)

		#US20
		veifyNoAuntUncleMarrNieceNephew(indiList, famList)

		#US21
		check_gender_roles(famList)

		#US22
		if uniqueID(indiList) != True:
			print('Repeated ID')
		else:
			pass

		#US23
		if uniqueNameAndBirthday(indiList) != True:
			print('WARN: IND: US23: Repeated Name and Birthday')
		else:
			pass

		#US24
		check_dupe_spouses(famList)

		#US25
		check_unique_child(famList)

		#US26
		verifyCorrespondingEntries(indiList, famList)

		#US27
		get_individual_age(indiList)

		#US29
		print("INFO: IND: US29: Deceased Records:")
		get_deceased_records(indiList)

		#US30
		get_living_married(indiList, famList)

		#US31
		get_living_single(indiList, famList)

		#US34
		get_large_age_diff(indiList, famList)

		#US35
		listRecentBirths(indiList)

		#US36
		findRecentDeath(indiList)

		#US38
		listUpcomingBirthdays(indiList)

		#US39
		upcomingAnni(famList)

		#US43
		FindChildrenBornBeforeParent(famList)

		#US44
		verifyNoGrandparentMarrGranchild(indiList, famList)

		#US45
		siblingAgeDiff(famList, indiList)

		#US46
		childParentAgeDiff(famList, indiList)

		#US48
		get_children_same_birthdays(indiList, famList)

		#US49
		findTwins(famList)

		#US50
		findTriplets(famList)

		#US51
		largestFamily(famList)

		#US52
		get_children_named_after_parent(indiList, famList)

		#US39
		upcomingAnni(famList)

		#US53
		sameName(indiDF)

		#US55
		listDeceasedDivor(indiDF, famList)

		#US57
		get_list_of_widow(indiList, famList)

		#US61
		get_list_of_oldest(indiList, famList)

		check_dupe_spouses(famList)



if __name__ == "__main__": 	# execute only if run as a script
	main()
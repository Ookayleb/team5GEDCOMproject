from prettytable import PrettyTable



def read_a_file():
	file = open('family_project.ged', 'r')
	Lines = file.readlines()
	tags = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT',
			'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB', 'WIFE',
			'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE']
	levels = ['0', '1', '2']

	words = []
	for line in Lines:
		word = line.split()
		words.append(word)

	#removing brackets
	new_words = [val for sub_person in words for val in sub_person]

	#finding the number of individuals
	ind_count = 0
	for ele in new_words:
		if ele == 'INDI':
			ind_count += 1
	

	#creating empty list for the number of individuals
	person = []
	for i in range(ind_count):
		person.append([])

	# Individuals index
	k = -1

	#Checking data from new_words list and appending the data to person list
	for j in range(len(new_words)):
		if(new_words[j] == "INDI"):
			k += 1
			person[k].append(new_words[j-1])
		if new_words[j] == 'NAME':
			person[k].append(new_words[j+1])
			person[k].append(new_words[j+2])
		if(new_words[j] == "SEX"):
			person[k].append(new_words[j+1])
		if(new_words[j] == "DATE" and new_words[j-2] == 'BIRT'):
			person[k].append(new_words[j+1])
			person[k].append(new_words[j+2])
			person[k].append(new_words[j+3])
		if(new_words[j] == 'DEAT'):
			person[k].append(new_words[j+1])
			person[k].append(new_words[j+2])
			person[k].append(new_words[j+3])
		if (new_words[j] == "FAMC"):
			person[k].append(new_words[j])
			person[k].append(new_words[j])
			person[k].append(new_words[j+1])
		if( new_words[j]=="FAMS"):
			person[k].append(new_words[j])
			person[k].append(new_words[j])
			person[k].append(new_words[j+1])

	#finding the number of families
	fam_count = 0
	for ele in new_words:
		if ele == 'FAM':
			fam_count += 1

	#creating empty list for the number of families
	family = []
	for i in range(fam_count):
		family.append([])

	#family index
	l = -1

	#Checking data from new_words list and appending the data to family list

	for j in range(len(new_words)):
		if(new_words[j] == "FAM"):
			l += 1
			family[l].append(new_words[j-1])
		if(new_words[j] == 'MARR'):
			family[l].append(new_words[j+3])
			family[l].append(new_words[j+4])
			family[l].append(new_words[j+5])
		if(new_words[j] == "DIV"):
			family[l].append(new_words[j+3])
			family[l].append(new_words[j+4])
			family[l].append(new_words[j+5])
	
		if (new_words[j] == "HUSB"):
			family[l].append(new_words[j+1])
		if (new_words[j] == "WIFE"):
			family[l].append(new_words[j+1])
		if (new_words[j] == "CHIL"):
			family[l].append(new_words[j+1])

	return person, family;


def print_individual_pretty_table():

	#Making prettytable structure
	x = PrettyTable()
	x.field_names = ['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse']
	persons = read_a_file()[0]

	#Getting record of each person
	for i in range(len(persons)):
		a_person = persons[i]

		#Checking if you are a child
		child = ""
		if (a_person[7] == 'FAMC'):
			child = a_person[9]
		else:
			child = 'NA'

		#checking if you are married
		spouse = ""
		if (a_person[7] == 'FAMS'):
			spouse = a_person[9]
		else:
			spouse = 'NA'


		#adding rows to the table
		x.add_row([a_person[0], a_person[1]+ ' ' +a_person[2], a_person[3], 
			a_person[5]+ ' ' + a_person[4] + ' ' + a_person[6], (2020 - int(a_person[6])),
			 'Yes', 'No', child,spouse])
	print(x)

print_individual_pretty_table()


def print_family_pretty_table():
	y = PrettyTable()
	y.field_names = ['ID', 'Married', 'Divorced', 'Husband ID', 'Wife ID', 'Children']
	families = read_a_file()[1]

	divorce = ""

	#print(families)
	for i in range(len(families)):
		family = families[i]
		y.add_row([family[0], family[1] + family[2] + family[3], 'NA', family[4], family[5], {family[6] + ', ' + family[7]}])
	print(y)


print_family_pretty_table()
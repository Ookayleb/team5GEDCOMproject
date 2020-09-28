from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar
import pandas as pd

def get_exactly_130_years_of_age():
	age_limit = 130
	one_thirty_age = (datetime.now() - relativedelta(years=age_limit)).strftime('%Y-%m-%d')
	return datetime.strptime(one_thirty_age, '%Y-%m-%d')

def get_number_month(letter_month):
	letter_month = letter_month.capitalize()
	abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
	return abbr_to_num[letter_month]

def turn_arr_into_date_arr(arr):
	return [arr[-1], get_number_month(arr[-2]), arr[0]]

def get_person_record():
	file = open('family_project.ged', 'r')
	Lines = file.readlines()
	tags = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT',
			'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB', 'WIFE',
			'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE']
	levels = ['0', '1', '2']




	individual = []
	a_person = []
	someone = []
	num_of_individual = 0

	for line in Lines:
		arr = line.split()
		if(len(arr) > 2):
			tag = arr[2]
		if tag == "INDI":
			num_of_individual += 1

	for i in range(num_of_individual):
		individual.append([])
		a_person.append([])
		someone.append([])	



	i = -1
	for line in Lines:
		arr = line.split()
		level = arr[0]
		tag = arr[1]
		arguments = arr[2:]

		for arg in arguments:
			if arg == "INDI":
				tag = arg
				arguments = arr[1]

		if tag == "INDI":
			i += 1
		individual[i].append({tag:arguments})


	for i in range(len(individual)):
		person = individual[i]
		for j in range(len(person)):
			obj = person[j]
			keys = obj.keys()
			values = obj.values()
			for key in keys:
				if key == "DATE":
					a_person[i].append({key: obj[key]})
				if key == "INDI":
					a_person[i].append({key:obj[key]})
				if key == "NAME":
					a_person[i].append({key:obj[key]})
				if key == "BIRT":
					a_person[i].append({key: True})

	for i in range(len(a_person)):
		try:
			elem0 = a_person[i][0]['INDI']
			elem1 = a_person[i][1]['NAME']
			elem2 = a_person[i][2]['BIRT']
			elem3 = a_person[i][3]['DATE']
		except IndexError:
			elem0 = "N/A"
			elem1 = "N/A"
			elem2 = "N/A"
			elem3 = "N/A"

		someone[i].append(elem0)
		someone[i].append(elem1)
		someone[i].append(elem2)
		someone[i].append(elem3)
	file.close()
	return someone

def print_age_qualification():

	person = get_person_record()
	one_hundred_and_thirty = get_exactly_130_years_of_age()
	each_person = []
	isQualified = ""

	for i in range(len(person)):
		if (person[i][2] == True):
			name_arr = person[i][1]
			date_arr = person[i][3]
			date_str = turn_arr_into_date_arr(date_arr)
			born_date = date_str[0] + '-' + str(date_str[1]) + '-' + str(date_str[2])
			curr_born_date = datetime.strptime(born_date, '%Y-%m-%d')
			name = ""
			for j in range(len(name_arr)):
				name += name_arr[j].strip("/") + " "
			if(curr_born_date >= one_hundred_and_thirty):
				isQualified = 'Yes'
				each_person.append([name, born_date,  isQualified])
			else:
				isQualified = 'No'
				each_person.append([name, born_date,  isQualified])
	return each_person

def print_data():
	person_record = print_age_qualification()
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

print(print_data())

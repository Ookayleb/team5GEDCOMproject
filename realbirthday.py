def realbirthday(rt, roots):
    for individual in indiList:
		if individual['Child'] is not 'NaN':
			indiID = individual['ID']
			childBirthday = lookup("Birthday", indiID)
			childFamilyID = lookup("Child", indiID)
	print("Birthday" + childBirthday + "")
	for family in famList:
		if family['Children'] is not 'NaN':
			#Checked for wife only, husband not required to be a parent.
			wifeID = family['Wife ID']
			wifeDeath = lookup("Death", indiID)
	print("Death" + wifeDeath + "")

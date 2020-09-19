# Jason Tran, William Martin, Caleb Choy, Jared Weinblatt, Sean James, Austin Luo
# I pledge my honor that I have abided by the Stevens Honor System
import sys
import re


#List of valid tags that should have Y
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

if(len(sys.argv) == 2):	#Check that we have 2 arguments
	with open(sys.argv[1], "r", encoding="utf8") as inFile:		#open the file provided in the argument

		for line in inFile:
			print("--> " + line.rstrip('\n'))

			level, tag, valid, arguments = "", "", "", ""
			tokenizedStr = re.search("(\d) (\S*) ?(.*)", line).groups()			#Use regex to store each token into a var. "1 NAME Bob /Smith/" becomes ["1", "NAME", "Bob /Smith/"]


			level	= tokenizedStr[0]

			#Check if third token is in the special list
			if tokenizedStr[2] in THIRD_TOKEN_TAGS:
				arguments	= tokenizedStr[1]	#if so, tag is actually the last token and arguments were the second argument
				tag 		= tokenizedStr[2]
			else:
				tag 		= tokenizedStr[1]
				arguments	= tokenizedStr[2]

			#Valid is Y if we find the tag in the list of valid tags
			valid 	= 'N' if tag not in VALID_TAGS else 'Y'

			#Check for invalid tags
			if (tag=='DATE' and level=='1')  or  (tag=='NAME' and level=='2'):
				valid = 'N'

			print("<-- " + level + "|" + tag + "|" + valid + "|" + arguments)

else:
	print("Please provide a GEDCOM file.\nUSAGE: python3 script.py path/to/file.ged")
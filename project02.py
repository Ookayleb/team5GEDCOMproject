# Caleb Choy - I pledge my honor that I have abided by the Stevens Honor System
import sys
import re

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
THIRD_TOKEN_TAGS =[
	'INDI',
	'FAM'
]

if(len(sys.argv) == 2):
	with open(sys.argv[1], "r", encoding="utf8") as inFile:

		for line in inFile:
			print("--> " + line.rstrip('\n'))

			level, tag, valid, arguments = "", "", "", ""
			tokenizedStr = re.search("(\d) (\S*) ?(.*)", line).groups()

			level	= tokenizedStr[0]

			if tokenizedStr[2] in THIRD_TOKEN_TAGS:
				arguments	= tokenizedStr[1]
				tag 		= tokenizedStr[2]
			else:
				tag 		= tokenizedStr[1]
				arguments	= tokenizedStr[2]

			valid 	= 'N' if tag not in VALID_TAGS else 'Y'
			if (tag=='DATE' and level=='1')  or  (tag=='NAME' and level=='2'):
				valid = 'N'

			print("<-- " + level + "|" + tag + "|" + valid + "|" + arguments)

else:
	print("Please provide a GEDCOM file.\nUSAGE: python3 project02.py path/to/file.ged")
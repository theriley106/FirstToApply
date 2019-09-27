import json
import os
import re

DB = json.load(open("db.json"))

def update_company():
	allLines = open("newTempReadme.md").read().split("\n")
	change = True
	for i, val in enumerate(allLines):
		if len(val) > 0:
			splitTable = val[1:].split("|")
			onlyNum = splitTable[0]
			# This means it's a line with the company Info
			if len(onlyNum) < 10 and len(splitTable) > 0:
				nums = re.findall("\d+", onlyNum)
				if len(nums) == 1:
					del splitTable[1]
					allLines[i] = "|" + " | ".join([str(x) for x in splitTable])
	if change == True:
		with open('newTempReadme.md','w') as f:
			f.write( '\n'.join(allLines) )

if __name__ == '__main__':
	update_company()
import os
import re

def update_company(companyId):
	allLines = open("README.md").read().split("\n")
	change = False
	for i, val in enumerate(allLines):
		if len(val) > 0:
			splitTable = val[1:].split("|")
			onlyNum = splitTable[0]
			# This means it's a line with the company Info
			if len(onlyNum) < 10 and len(splitTable) > 0:
				nums = re.findall("\d+", onlyNum)
				if len(nums) == 1:
					if nums[0] == companyId:
						change = True
						splitTable[3] = "AYYYYY"
						allLines[i] = "|" + "|".join(splitTable) + "|"
						break
	if change == True:
		with open('filename.md','w') as f:
			f.write( '\n'.join(allLines) )

if __name__ == '__main__':
	update_company("3010")
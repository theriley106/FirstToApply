import os
import re
import json
import time

def update_company(companyId):
	db = json.load(open("db.json"))
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
						companyName = db.get(companyId).get("companyName")
						companyURL = db.get(companyId).get("url", "http://www.google.com")
						splitTable[2] = "[{}]({})".format(companyName, companyURL)
						splitTable[3] = db.get(companyId).get("count_intern", 0)
						splitTable[4] = db.get(companyId).get("count_2019", 0)
						splitTable[5] = db.get(companyId).get("ss_size", 0)
						splitTable[6] = int(time.time())
						allLines[i] = "|" + " | ".join([str(x) for x in splitTable])
						break
	if change == True:
		with open('filename.md','w') as f:
			f.write( '\n'.join(allLines) )

if __name__ == '__main__':
	update_company("3010")
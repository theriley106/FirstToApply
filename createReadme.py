# This program creates the readme from the companies file
import os
import time

readmeFile = open("template.md").read()
companyList = open("companies.txt").read().split("\n")
x = list(set(companyList))
companyList = sorted([g.title() for g in x])
os.system("touch newReadme.md && rm newReadme.md")

row = '| {} | {} | {} | {} | {} | {} | {} |'

toAdd = []
toAdd.append('| ID | Company Name | Link | Intern[ship] Count | 2019 Count | Verification | Updated |')
toAdd.append("| --------- | ------------- | --------------- | --------- | --------- | --------- | --------- |")

def get_link(company):
	return "[{} Jobs](http://www.google.com)".format(company)

def get_count(word):
	return 0

def get_verification_score(company):
	return 3


for i, company in enumerate(companyList):
	if len(company) > 0:
		idVal = str(i+1001).zfill(4)
		link = get_link(company)
		internCount = get_count("intern")
		yearCount = get_count("2019")
		verificationScore = get_verification_score(company)
		temp = row.format(idVal, company, link, internCount, yearCount, verificationScore, int(time.time()))
		toAdd.append(temp)

for val in toAdd:
	os.system('echo "{}" >> newReadme.md'.format(val))



import json


COMPANIES = open("companies.txt").read().split("\n")

'''
{
	"ss_size": 0,
	"count_2019": 0,
	"count_intern": 0
}

'''
if __name__ == '__main__':
	companyData = {}
	for val in COMPANIES:
		if len(val) > 0:
			companyData[val] = {
				"ss_size": 0,
				"count_2019": 0,
				"count_intern": 0
			}

	with open('data.json', 'w') as f:
		json.dump(companyData, f, indent=4)




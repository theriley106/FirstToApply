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
	for val in COMPANIES:
		print(val)
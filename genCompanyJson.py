import json


COMPANIES = open("companies.txt").read().split("\n")
if __name__ == '__main__':
	for val in COMPANIES:
		print(val)
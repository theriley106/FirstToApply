# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import requests

# This programs pulls company names from Jumpstart

url = "https://backend.jumpstart.me/api/company-roles/filter_list"

res = requests.get(url)

for val in res.json()['filters']['jobs'][5]['options']:
	print val['name']
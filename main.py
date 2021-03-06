# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import requests
import re
import json
import bs4
import os
import time
from selenium import webdriver

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

options = Options()
options.headless = True

firefoxProfile = webdriver.FirefoxProfile()
firefoxProfile.set_preference("http.response.timeout", 10)

driver = webdriver.Firefox(options=options, firefox_profile=firefoxProfile)


DB = json.load(open("db.json"))

def extract_companies():
	return json.load(open("links.json"))

def extract_urls(fileName):
	a = open(fileName).read()
	url_re = re.compile(r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))')
	for match in url_re.finditer(a):
		yield match.group(0)

def extract_urls_from_text(a):
	url_re = re.compile(r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))')
	for match in url_re.finditer(a):
		yield match.group(0)

def grabSite(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	return requests.get(url, headers=headers)

def airbnb():
	url = "https://careers.airbnb.com/university/"
	res = grabSite(url)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	return str(page).count("2020") > 0

def akuna():
	url = "https://akunacapital.com/wp-admin/admin-ajax.php?action=gh_ajax_request&experience=Intern&department=&location="
	res = grabSite(url).json()
	#print(len(res['matched_jobs']))
	return len(res['matched_jobs']) != 14

def dropbox():
	url = "https://www.dropbox.com/jobs/teams/eng_university_grads#open-positions"
	res = grabSite(url)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	#print len(page.select(CSS))
	if len(page.select(".open-positions__listing")) != 1:
		return True
	if len(page.select(".open-positions__listing")) > 0:
		if 'summer' not in str(page.select(".open-positions__listing")[0]).lower():
			return True
	return False

def duolingo():
	url = "https://www.duolingo.com/jobs_list"
	res = grabSite(url)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	return str(page).count("2020") > 0

def spacex():
	url = "https://www.spacex.com/careers/list?field_job_category_tid%5B%5D=966&type%5B%5D=37"
	res = grabSite(url)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	return len(page.select(".views-field-title")) > 0

def slack():
	url = "https://slack.com/careers/university-recruiting"
	res = grabSite(url)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	#print str(page).count("2020")
	return str(page).count("2020") > 0

def nextdoor():
	url = "https://boards.greenhouse.io/embed/job_board?for=nextdoor&b=https%3A%2F%2Fnextdoor.com%2Fjobs%2F"
	res = grabSite(url)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	#print str(page).count("2019")
	return str(page).count("2020") > 0

def stripe():
	url = "https://stripe.com/jobs/search?s=intern"
	res = grabSite(url)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	#print(str(page).count("intern"))
	return str(page).count("intern") != 1008

def uber():
	url = "https://www.uber.com/careers/list/?city=all&country=all&keywords=&subteam=all&team=university&iisc=Website&iisn=Website&iis=University-Careers-Page"
	res = grabSite(url)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	return len(page.select(".flush--bottom")) > 30

def yext():
	#print("Checking Yext")
	url = "https://boards.greenhouse.io/yext"
	res = grabSite(url)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	#print str(page).count("2019")
	return str(page).count("2020") > 0

"""
COMPANY_LIST = []

COMPANY_LIST.append({'company': 'airbnb', 'function': airbnb})
COMPANY_LIST.append({'company': 'akuna', 'function': akuna})
COMPANY_LIST.append({'company': 'dropbox', 'function': dropbox})
COMPANY_LIST.append({'company': 'duolingo', 'function': duolingo})
COMPANY_LIST.append({'company': 'spacex', 'function': spacex})
COMPANY_LIST.append({'company': 'slack', 'function': slack})
COMPANY_LIST.append({'company': 'nextdoor', 'function': nextdoor})
COMPANY_LIST.append({'company': 'stripe', 'function': stripe})
COMPANY_LIST.append({'company': 'uber', 'function': uber})
COMPANY_LIST.append({'company': 'yext', 'function': yext})
"""


def check_new(url, count1, count2, company):
	#res = grabSite(url)
	driver.get(url)
	driver.save_screenshot("{}.png".format(company))
	page = bs4.BeautifulSoup(driver.page_source, 'lxml')
	if len(raw_input("Click to Continue")) > 0:
		return True
	else:
		return False
	return str(page).count("2020") > count1 or str(page).lower().count("intern")

def do_all():
	for company in COMPANY_LIST:
		if company['function']():
			print("{} IS OPEN".format(company['company']))

def search(searchTerm):
	try:
		driver.set_page_load_timeout(10)
		driver.get("https://www.google.com/search?&q={}&btnI".format(searchTerm.replace(" ", "+")))
	except Exception:
		print 'time out'
		webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
	

def click_first_link():
	results = driver.find_elements_by_xpath('//div[@class="r"]/a/h3')
	results[0].click()

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
		with open('README.md','w') as f:
			f.write( '\n'.join(allLines) )

def update(companyCode):
	try:
		if companyCode not in DB:
			print("{} DOES NOT EXIST".format(companyCode))
			return
		info = dict(DB[companyCode])
		company = info['companyName']
		search(company + " internships")
		info['count_intern'] = str(driver.page_source).count('intern')
		info['count_2019'] = str(driver.page_source).count('2020')
		info['url'] = driver.current_url
		driver.save_screenshot('temp.png')
		info['ss_size'] = os.path.getsize('temp.png')
		if DB[companyCode].get("count_intern", "O") != info['count_intern']:
			print("{} IS OPEN".format(company))
		elif DB[companyCode].get("count_2019", "O") != info['count_2019']:
			print("{} IS OPEN".format(company))
		elif float(abs(DB[companyCode].get("ss_size", -500) - info['ss_size'])) / float(info['ss_size']) > .05:
			print("{} IS OPEN".format(company))
		DB[companyCode] = info
		with open('db.json', 'w') as outfile:
			json.dump(DB, outfile, indent=4)
		print("Updated {}".format(company))
		os.system("rm temp.png")
		# update_company(companyCode)
	except Exception as exp:
		print("ERROR")
		print(exp)

if __name__ == '__main__':
	companies = sys.argv[1:]
	if "--all" in str(companies).lower():
		companies = sorted(DB.keys())
	if len(companies) == 0:
		while True:
			update(raw_input("Company Code: "))
		for val in extract_companies():
			if check_new(val['url'], val['2020'], val['intern'], val['company']):
				print("{} IS OPEN".format(val['company']))
	else:
		count = 0
		for val in companies:
			update(val)
			count += 1
			if count % 20 == 0:
				print("Finished {}".format(count))
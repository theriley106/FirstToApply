from selenium import webdriver
import json

try:
    input = raw_input
except NameError:
    pass

driver = webdriver.Firefox()




def search(searchTerm):
	driver.get("https://www.google.com/search?&q={}".format(searchTerm.replace(" ", "+")))

def click_first_link():
	results = driver.find_elements_by_xpath('//div[@class="r"]/a/h3')  # finds webresults
	results[0].click()

if __name__ == '__main__':
	db = json.load(open("links.json"))
	while True:
		company = input("Company: ")
		if len(company) == 0:
			driver.quit()
			break
		search(company + " internships")
		click_first_link()
		input("Press enter when done")
		print("2020 Count: {}".format())
		print("Intern Count: {}".format(str(driver.page_source).count('intern')))
		info = {}
		info['company'] = company
		info['2020'] = str(driver.page_source).count('2020')
		info['intern'] = str(driver.page_source).lower().count('intern')
		info['url'] = driver.current_url
		db.append(info)
		with open('links.json', 'w') as outfile:
		    json.dump(db, outfile)

from selenium import webdriver

driver = webdriver.Firefox()


def search(searchTerm):
	driver.get("https://www.google.com/search?&q={}".format(searchTerm.replace(" ", "+")))

def click_first_link():
	results = driver.find_elements_by_xpath('//div[@class="r"]/a/h3')  # finds webresults
	results[0].click()

if __name__ == '__main__':
	while True:
		company = input("Company: ")
		if len(company) == 0:
			driver.quit()
			break
		search(company + " internships")
		input("Press enter when done")

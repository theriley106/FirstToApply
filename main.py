import requests
import praw
import re
import json
import bs4
try:
	from keys import *
except:
	REDDIT_ID = input("REDDIT ID: ")
	REDDIT_CLIENT_SECRET = input("REDDIT CLIENT SECRET: ")

def extract_from_reddit(idVal="9nb0vb"):
	url = "https://api.pushshift.io/reddit/submission/comment_ids/{}".format(idVal)
	res = requests.get(url)
	#print res.json()

def extract_urls(fileName):
	a = open(fileName).read()
	url_re = re.compile(r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))')
	for match in url_re.finditer(a):
		yield match.group(0)

def extract_urls_from_text(a):
	url_re = re.compile(r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))')
	for match in url_re.finditer(a):
		yield match.group(0)

def extract_all_comments(postID='914rhn'):
	commentList = []
	reddit = praw.Reddit(
		client_id=REDDIT_ID,
		client_secret=REDDIT_CLIENT_SECRET,
		user_agent='internship search')

	submission = reddit.submission(id=postID)

	submission.comments.replace_more(limit=None)
	comment_queue = submission.comments[:]  # Seed with top-level
	while comment_queue:
		comment = comment_queue.pop(0)
		lVal = []
		for val in extract_urls_from_text(comment.body):
			lVal.append(val)
		commentList.append({"urls": lVal, "body": comment.body, "date": comment.created_utc})
		comment_queue.extend(comment.replies)
	return commentList

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
		

COMPANY_LIST = []

COMPANY_LIST.append({'company': 'airbnb', 'function': airbnb})
COMPANY_LIST.append({'company': 'akuna', 'function': akuna})
COMPANY_LIST.append({'company': 'dropbox', 'function': dropbox})
COMPANY_LIST.append({'company': 'duolingo', 'function': duolingo})
COMPANY_LIST.append({'company': 'spacex', 'function': spacex})
COMPANY_LIST.append({'company': 'slack', 'function': slack})


def do_all():
	for company in COMPANY_LIST:
		if company['function']():
			print("{} IS OPEN".format(company['company']))


if __name__ == '__main__':
	do_all()
	'''a = extract_all_comments()
				with open('outputfile.json', 'w') as fout:
					json.dump(a, fout, indent=4)'''
	#for val in extract_urls('comments2.txt'):
	#	print(val)

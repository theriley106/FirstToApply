import requests
import praw
try:
	from keys import *
except:
	REDDIT_ID = input("REDDIT ID: ")
	REDDIT_CLIENT_SECRET = input("REDDIT CLIENT SECRET: ")

def extract_from_reddit(idVal="9nb0vb"):
	url = "https://api.pushshift.io/reddit/submission/comment_ids/{}".format(idVal)
	res = requests.get(url)
	#print res.json()

import praw

reddit = praw.Reddit(
	client_id=REDDIT_ID,
	client_secret=REDDIT_CLIENT_SECRET,
	user_agent='internship search')

submission = reddit.submission(id='914rhn')

submission.comments.replace_more(limit=None)
comment_queue = submission.comments[:]  # Seed with top-level
while comment_queue:
	comment = comment_queue.pop(0)
	print(comment.body)
	comment_queue.extend(comment.replies)
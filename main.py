import requests

def extract_from_reddit(idVal="9nb0vb"):
	url = "https://api.pushshift.io/reddit/submission/comment_ids/{}".format(idVal)
	res = requests.get(url)
	print res.json()

if __name__ == '__main__':
	extract_from_reddit()
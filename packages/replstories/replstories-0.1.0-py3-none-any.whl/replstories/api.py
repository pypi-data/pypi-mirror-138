import requests

def getallposts():
	res = requests.post("https://api.replstories.xyz/getallposts")
	json = res.json()
	return json

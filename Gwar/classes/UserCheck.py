import requests
import json

class UserCheck():

	def search(self, username):
		self.username = username
		res=[]

		#CHECKS

		#GITHUB
		if(self.check_github()): 
			res.append(["GitHub", "https://github.com/"+self.username])
			print("[UserCheck] Found github match!")

		#TWITTER
		for t in self.check_twitter(): 
			res.append(["Twitter", t])
			print("[UserCheck] Found Twitter match!")

		#INSTAGRAM
		if(self.check_instagram()): 
			res.append(["Instagram", "https://www.instagram.com/"+self.username+"/?hl=es"])
			print("[UserCheck] Found Instagram match!")

		#YOUTUBE
		if(self.check_youtube()): 
			res.append(["YouTube", "https://www.youtube.com/user/"+self.username])
			print("[UserCheck] Found YouTube match!")

		#REDDIT
		if(self.check_reddit()): 
			res.append(["Reddit", "https://www.reddit.com/user/"+self.username])
			print("[UserCheck] Found Reddit match!")
		
		#ASK
		#GMAIL
		#FLICKR
		#500PX
		#SOUNDCLOUD
		#DEVIANART
		#LAST.FM

		return res
		
	def check_github(self):
		r = requests.get("https://github.com/"+self.username)
		if(r.status_code==404 or r.status_code=="404"):
			return False
		return True

	def check_twitter(self):
		cookies = {}
		headers = {"x-csrf-token": "badf398ecf3cbb76a0b6556a94e3ed52", "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"}
		aux_cookies = 'personalization_id="v1_UQxVkx6dhJlgx3gC5eJfmA=="; guest_id=v1%3A157052024323215768; _ga=GA1.2.579175285.1570520243; eu_cn=1; des_opt_in=Y; dnt=1; ads_prefs="HBESAAA="; kdt=Vm4voRhCr2OH8ZB4heMaGfI3aOevYIpin8xaftvj; remember_checked_on=1; twid=u%3D449117299; auth_token=91e9ef404f0c07deb8648261fc48159b57b2e232; _twitter_sess=BAh7DSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ACIJcHJycCIAOg9jcmVhdGVkX2F0bCsIBeyEr20B%250AOgxjc3JmX2lkIiU3NWQzYzRmMjZlMTgyNzY0NmZiYWQ4YTM0Y2MzYWJiNToH%250AaWQiJTBhMzYxMTc3OThiZjg3OTQ4MGM5Y2JlZjk3Y2Y4NzgwOghwcnNpCDoI%250AcHJ1bCsJAJCWhVqcgg06CHByaWkH--ff200394fa03ce11fd3aaf691eca4825441f071e; csrf_same_site_set=1; csrf_same_site=1; rweb_optin=side_no_out; ct0=badf398ecf3cbb76a0b6556a94e3ed52; _gid=GA1.2.587847043.1570704873; external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|8e8t2xd8A2w%3D'
		for c in aux_cookies.split("; "):
			d = c.split("=")
			cookies[d[0]]=d[1].replace('"', "")
		r = requests.get("https://api.twitter.com/1.1/search/typeahead.json?q="+self.username+"&src=search_box&result_type=events%2Cusers%2Ctopics", cookies=cookies, headers=headers)
		for user in json.loads(r.content.decode())["users"]:
			yield "https://twitter.com/"+user["screen_name"]

	def check_instagram(self):
		r = requests.get("https://www.instagram.com/"+self.username+"/?hl=es")
		if(r.status_code == 200 or r.status_code == "200"):
			return True
		return False

	def check_youtube(self):
		r = requests.get("https://www.youtube.com/user/"+self.username)
		if(r.status_code == 200 or r.status_code == "200"):
			return True
		return False

	def check_reddit(self):
		r = requests.get("https://www.reddit.com/user/"+self.username, allow_redirects=True, headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"})
		if(r.status_code == 200 or r.status_code == "200"):
			return True
		return False
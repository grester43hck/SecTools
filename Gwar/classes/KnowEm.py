import requests

class KnowEm():

	def search(self, username):
		platforms = ["Blogger", "facebook", "Flickr", "Imgur", "Instagram", "LinkedIn", "MySpace", "Pinterest", "reddit", "soundcloud", "Tumbrl", "YouTube", "Vimeo", "github", "Wordpress"]
		res=[]
		for p in platforms:
			if(self.check(p, username)):
				res.append(p)
				print("[KnowEm] Found "+p)
		return res

	def check(self, p, username):
		if("Sorry" in requests.get("https://knowem.com/usercheckv2.php?target="+p+"&username="+username, headers={"X-Requested-With": "XMLHttpRequest"}).content.decode()): return True
		return False
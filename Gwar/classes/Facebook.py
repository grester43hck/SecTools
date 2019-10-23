import requests
import json

class Facebook():
	def __init__(self, user=None, url=None):
		if(user!=None): self.url = "https://www.facebook.com/"+user+"/"
		if(url!=None): self.url = url

	def get_data(self):
		aux = requests.get(self.url).content
		try:
			self.content = aux.decode().split('<script type="application/ld+json">')[1].split("</script>")[0]
			res = json.loads(self.content)
			print("[Facebook] RAW: "+str(res))
			result = {}
			try:
				result["type"]=res["\u0040type"]
			except:
				pass
			try:
				result["name"]=res["name"]
			except:
				pass
			try:
				print("[Facebook] Found job title: "+res["jobTitle"])
				result["jobTitle"]=res["jobTitle"]
			except:
				pass
			try:
				print("[Facebook] Found address: "+str(res["address"]))
				result["address"]=res["address"]
			except:
				pass
			try:
				print("[Facebook] Found affiliation: "+res["affiliation"])
				result["affiliation"]=res["affiliation"]
			except:
				pass
			return result
		except:
			return {}


FB = Facebook(url="https://www.facebook.com/profile.php?id=100003182351885")
print(FB.get_data())
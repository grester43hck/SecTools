import requests
import json

class Twitter():

	languages=[]
	names=[]
	profile_imgs=[]
	quoted_users=[]
	replied_users=[]
	retweeted_users=[]
	apps=[]
	hostnames=[]
	usernames=[]
	dates=[]
	texts=[]

	def __init__(self, user):
		value = input("accountanalysis cookie: ")
		self.user = user
		self.cookies = {"accountanalysis":value}

	def text_to_words(self, text):
		simbols=[".", "?", "¿", "%", "$"]
		for s in simbols:
			text=text.replace(s, "")
		return text.split(" ")

	def get_data(self):
		self.userdata = json.loads(requests.get("https://accountanalysis.app/api/twitter/user?username="+self.user, cookies=self.cookies).content.decode())
		
		self.tweets = json.loads(requests.get("https://accountanalysis.app/api/twitter/tweets?username="+self.user, cookies=self.cookies).content.decode())
		print("[Twitter] Found "+str(len(self.tweets)) + " (max 200) tweets on the account, starting analysis...")

		date_res = {}
		weekday_res = {"Mon":0, "Tue":0, "Wed":0, "Thu":0, "Fri":0, "Sat":0, "Sun":0}
		for i in range(0, 24):
			date_res[str(i)]=0

		for t in self.tweets:
			if(t["language"] not in self.languages): self.languages.append(t["language"])
			if(t["name"] not in self.names): self.names.append(t["name"])
			if(t["profileImageUrl"] not in self.profile_imgs): self.profile_imgs.append(t["profileImageUrl"])
			if(t["quotedUser"] not in self.quoted_users): self.quoted_users.append(t["quotedUser"])
			if(t["repliedUser"] not in self.replied_users): self.replied_users.append(t["repliedUser"])
			if(t["retweetedUser"] not in self.retweeted_users): self.retweeted_users.append(t["retweetedUser"])
			if(t["usedApp"] not in self.apps): self.apps.append(t["usedApp"])
			for uh in t["usedHostnames"]:
				if(uh not in self.hostnames): self.hostnames.append(uh)
			if(t["username"] not in self.usernames): self.usernames.append(t["username"])
			print(t["timestamp"])
			hour = t["timestamp"].split(" ")[3].split(":")[0]
			weekday = t["timestamp"].split(" ")[0]
			if(hour!="00"): hour=hour.replace("0", "")
			else: hour="0"
			date_res[str(hour)]+=1
			weekday_res[str(weekday)]+=1

			self.texts.append(t["text"])

		words = {}
		for t in self.texts:
			for w in self.text_to_words(t):
				try:
					words[w]+=1
				except:
					words[w]=1


		res={
		"languages":self.languages,
		"names":self.names,
		"profileImages": self.profile_imgs,
		"quotedUsers": self.quoted_users,
		"repliedusers": self.replied_users,
		"apps": self.apps,
		"hostnames": self.hostnames,
		"usernames": self.usernames,
		"activeHours": date_res,
		"activeWeekDays": weekday_res
		}

		return res

FB = Twitter(input("twitter user: "))
print(FB.get_data())
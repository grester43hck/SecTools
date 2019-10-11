from classes.GoogleDocumentFinder import GoogleDocumentFinder
from classes.LibreBorne import LibreBorne
from classes.IntelligenceX import IntelligenceX
from classes.Linkedin import Linkedin
from classes.UserCheck import UserCheck

from prettytable import PrettyTable
import operator
import subprocess as sp


class GWar():

	user_vars={}
	prompt="[GWar]==> "
	help_text = '''
	##CORE 
	set {var} {value} #set the variable toa value as default for all commands
	db_show {list/command/*} #shows the session results of a command or all commands
	verify {var} {value} #set a value as verified for the target
	profile #shows the target verified info profile

	##Verify:
	##This info serves for later investigation on verified info about the target
	##Also makes the info that shows in the profile command

	##PERSONAL INFO
	find_persona {first_name} {second_name} #LibreBorme search
	find_doc {first_name} {second_name} #Document search on google
	intel_email {email} #Search for email leaks on IntelligenceX
	link_persona {first_name} {second_name} #Search in LinkedIn <-- CURRENTLY NOT WORKING

	##ENTERPRISE INFO
	find_empresa {name} #Libreborme search

	#USERNAME INFO
	find_user {username} #Check for username in different platforms and social networks
	'''
	banner='''

                                                              
  ,----..               .---.                                 
 /   /   \             /. ./|                                 
|   :     :        .--'.  ' ;                 __  ,-.            ,a888a,            88 
.   |  ;. /       /__./ \ : |               ,' ,'/ /|          ,8P"' `"Y8,        ,d88 
.   ; /--`    .--'.  '   \' .    ,--.--.    '  | |' |          ,8P       Y8,      88888 
;   | ;  __  /___/ \ |    ' '   /       \   |  |   ,'         `8b       d8'         88 
|   : |.' .' ;   \  \;      :  .--.  .-. |  '  :  /            `8ba, ,ad8'   d8     88 
.   | '_.' :  \   ;  `      |   \__\/: . .  |  | '               "Y888P"     Y8     88
'   ; : \  |   .   \    .\  ;   ," .--.; |  ;  : |            
'   | '/  .'    \   \   ' \ |  /  /  ,.  |  |  , ;            
|   :    /       :   '  |--"  ;  :   .'   \  ---'             
 \   \ .'         \   \ ;     |  ,     .-./                   
  `---`            '---"       `--`---'                       
                                                              

	'''

	def __init__(self):
		tmp = sp.call('cls',shell=True)
		self.exit=False
		self.db={}
		self.profile={}
		self.init()

	def init(self):
		print(self.banner)
		while(not self.exit):
			com = input(self.prompt)
			res, self.exit = self.process_com(com)
			print(res)

	def process_com(self, com):
		exit = False
		com = com.lower()
		com = com.split(" ")
		res=""

		if(com[0]=="exit" or com[0]=="quit" or com[0]=="q"):
			print("Exiting GWar, bye!")
			exit=True

		if(com[0]=="h" or com[0]=="help"):
			res = self.help_text

		if(com[0]=="db_show"):
			res = self.get_db(com)

		if(com[0]=="set"):
			self.user_vars[com[1]]=" ".join(com[2:])
			print("[GWar] Setted "+com[1]+" to value "+self.user_vars[com[1]])

		if(com[0]=="verify"):
			self.profile[com[1]]=" ".join(com[2:])
			print("[GWar] Verified "+com[1]+" to value "+self.profile[com[1]])

		if(com[0]=="profile"):
			res = self.show_profile(com)

		if(com[0]=="cls"):
			tmp = sp.call('cls',shell=True)
			print(self.banner)

		if(com[0]=="find_doc"):
			res = self.find_doc(com)

		if(com[0]=="find_persona"):
			res = self.find_persona(com)

		if(com[0]=="find_empresa"):
			res = self.find_empresa(com)

		if(com[0]=="intel_email"):
			res = self.intel_email(com)

		if(com[0]=="link_persona"):
			res = self.link_persona(com)

		if(com[0]=="find_user"):
			res = self.find_user(com)


		if(res=="" and not exit):
			res="type help (h) for a list of commands"
		return res, exit

	def show_profile(self, com):
		res=PrettyTable()
		res.field_names = ["Key", "Value"]
		for key, val in self.profile.items():
			res.add_row([key, val])
		return res

	def save_item(self, key, item):
		try:
			if(item not in self.db[key]): 
				self.db[key].append(item)
		except:
			self.db[key]=[item]

	def get_db(self, com):
		res=""
		if(com[1]=="list"):
			for key, value in self.db.items():
				res+="[+] db_show "+key+"\n"
			res+="[+] db_show * (for all saved items)\n"

		if(com[1]=="*"):
			for key, value in self.db.items():
				res+="\n ############### "+key+" ###############\n\n"
				aux = PrettyTable()
				for v in value:
					aux.add_row(v)
				res+=aux.get_string()

		if(com[1] in self.db.keys()):
			aux = PrettyTable()
			for v in self.db[com[1]]:
				aux.add_row(v)
			res+=aux.get_string()

		return res

	def find_doc(self, com):
		if(len(com)==1):
			try:
				com=["find_doc", self.user_vars["first_name"], self.user_vars["second_name"]]
				print("command arguments setted from this session user variables ("+str(self.user_vars)+")")
			except:
				pass
		res = PrettyTable()
		res.field_names = ["Domain", "Link"]

		for a in GoogleDocumentFinder(first_name=com[1], second_name=" ".join(com[2:])).search():
			dom = a.replace("http://", "").replace("https://", "").split("/")[0]
			self.save_item("find_doc", [dom, a])
			res.add_row([dom, a]) 
		return res

	def find_persona(self, com):
		if(len(com)==1):
			try:
				com=["find_persona", self.user_vars["first_name"], self.user_vars["second_name"]]
				print("command arguments setted from this session user variables ("+str(self.user_vars)+")")
			except:
				pass
		LB = LibreBorne()
		result = LB.search_persona(com[1]+" "+" ".join(com[2:]))
		cont = 0
		slugs = []
		for r in result["objects"]:
			print(str(cont)+"- "+ r["name"] + " ("+r["slug"]+")")
			slugs.append(r["slug"])
			cont+=1
		if(len(result["objects"])>0):
			n = input("select a number: ")
			result = LB.get_info_persona(slugs[int(n)])
			res = PrettyTable()
			res.field_names = ["Dates", "Title", "Enterprise"]
			for c in result["cargos_actuales"]:
				res.add_row([c["date_from"] + " <--> NOW",c["title"],c["name"]])
				self.save_item("find_persona", [c["date_from"] + " <--> NOW",c["title"],c["name"]])

			for c in result["cargos_historial"]:
				res.add_row([c["date_from"] + " <--> "+c["date_to"],c["title"],c["name"]])
				self.save_item("find_persona", [c["date_from"] + " <--> "+c["date_to"],c["title"],c["name"]])

		else:
			res="No results"

		return res

	def find_empresa(self, com):
		if(len(com)==1):
			try:
				com=["find_persona", self.user_vars["first_name"], self.user_vars["second_name"]]
				print("command arguments setted from this session user variables ("+str(self.user_vars)+")")
			except:
				pass
		LB = LibreBorne()
		result = LB.search_ent(" ".join(com[1:]))
		cont = 0
		slugs = []
		for r in result["objects"]:
			print(str(cont)+"- "+ r["name"] + " ("+r["slug"]+")")
			slugs.append(r["slug"])
			cont+=1
		if(len(result["objects"])>0):
			n = input("select a number: ")
			result = LB.get_info_ent(slugs[int(n)])
			res = PrettyTable()
			res.field_names = ["Dates", "Title", "Enterprise"]
			for c in result["cargos_actuales_c"]+result["cargos_actuales_p"]:
				res.add_row([c["date_from"] + " <--> NOW",c["title"],c["name"]])
				self.save_item("find_empresa", [c["date_from"] + " <--> NOW",c["title"],c["name"]])

			for c in result["cargos_historial_c"]+result["cargos_historial_p"]:
				try:
					res.add_row([c["date_from"] + " <--> "+c["date_to"],c["title"],c["name"]])
					self.save_item("find_empresa", [c["date_from"] + " <--> "+c["date_to"],c["title"],c["name"]])
				except:
					res.add_row(["??? <--> "+c["date_to"],c["title"],c["name"]])
					self.save_item("find_empresa", ["??? <--> "+c["date_to"],c["title"],c["name"]])

			print(res)
			res=PrettyTable()
			res.field_names = ["cve", "url"]
			for c in result["in_bormes"]:
				res.add_row([c["cve"],c["url"]])
				self.save_item("bormes", [c["cve"],c["url"]])
		else:
			res="No results"

		return res

	def intel_email(self, com):
		if(len(com)==1):
			try:
				com=["intel_email", self.user_vars["email"]]
				print("command arguments setted from this session user variables ("+str(self.user_vars)+")")
			except:
				pass

		aux_res = IntelligenceX().search_email(com[1])
		res=PrettyTable()
		res.field_names = ["Leak", "Data"]
		for r in aux_res:
			res.add_row(r)
			self.save_item("intel_email", r)

		if(len(aux_res)>0):
			return res
		else:
			return "No results for email: "+com[1]

	def link_persona(self, com):
		if(len(com)==1):
			try:
				com=["find_persona", self.user_vars["first_name"], self.user_vars["second_name"]]
				print("command arguments setted from this session user variables ("+str(self.user_vars)+")")
			except:
				pass
		aux_res = Linkedin().search_persona(com[1], " ".join(com[2:]))
		cont=0
		aux_cache=[]
		for element in aux_res["data"]["elements"]:
			if(len(element["elements"])):
				for e in element["elements"]:
					print(str(cont)+"- "+e["title"]["text"] + " ("+e["navigationUrl"]+")")
					aux_cache.append(e["navigationUrl"])

		if(len(aux_cache)>0):
			n = input("select a number: ")

		else:
			res="No results"
		return res

	def find_user(self, com):
		if(len(com)==1):
			try:
				com=["find_persona", self.user_vars["username"]]
				print("command arguments setted from this session user variables ("+str(self.user_vars)+")")
			except:
				pass

		aux_res = UserCheck().search(com[1])
		res=PrettyTable()
		res.field_names = ["Platform", "Link"]
		for r in aux_res:
			res.add_row(r)
			self.save_item("find_user", r)

		return res


GWar()

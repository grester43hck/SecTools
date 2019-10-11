from classes.GoogleSearcher import GoogleSearcher

class GoogleDocumentFinder():
	def __init__(self, first_name, second_name, files=["pdf", "txt"]):
		self.first_name = first_name.title()
		self.second_name = " ".join([a.title() for a in second_name.split(" ")])
		self.files = files

	def search(self):
		q=[]
		#"first_name, second_name"
		q.append('"'+self.first_name + ", " + self.second_name + '"')
		#"second_name, first_name"
		q.append('"'+self.second_name + ", " + self.first_name + '"')
		for t in self.files:
			#"first_name, second_name" type:pdf
			q.append('"'+self.first_name + ", " + self.second_name + '"' + " file:"+t)
			#"second_name, first_name" type:pdf
			q.append('"'+self.second_name + ", " + self.first_name + '"' + " file:"+t)
		return GoogleSearcher(q).search(stop=7)
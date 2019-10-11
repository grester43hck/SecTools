from googlesearch import search
class GoogleSearcher():

	def __init__(self, queries):
		self.queries=queries

	def search(self, tld="com", stop=10, pause=2):
		cache=[]
		for q in self.queries:
			print("[GoogleSearch] Searching for: "+q)
			for j in search(q, tld=tld, stop=stop, pause=pause): 
				print("[GoogleSearch][("+q+")] "+"Found result: " + j)
				if(j not in cache):
					cache.append(j)
					yield j
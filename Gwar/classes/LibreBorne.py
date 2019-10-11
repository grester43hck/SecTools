import requests
import json

class LibreBorne():

	search = "https://librebor.me/borme/api/v1/{kind}/search/?q={name}"
	get_info = "https://librebor.me/borme/api/v1/{kind}/{slug}/"

	def do_req(self, url):
		return requests.get(url).content

	def search_persona(self, q):
		print("[LibreBorme] Searching for: "+q)
		res = self.do_req(self.search.replace("{kind}", "persona").replace("{name}", q))
		return json.loads(res)

	def get_info_persona(self, slug):
		print("[LibreBorme] Getting info from: "+slug)
		return json.loads(self.do_req(self.get_info.replace("{kind}", "persona").replace("{slug}", slug)))

	def search_ent(self, q):
		print("[LibreBorme] Searching for: "+q)
		res = self.do_req(self.search.replace("{kind}", "empresa").replace("{name}", q))
		return json.loads(res)

	def get_info_ent(self, slug):
		print("[LibreBorme] Getting info from: "+slug)
		return json.loads(self.do_req(self.get_info.replace("{kind}", "empresa").replace("{slug}", slug)))
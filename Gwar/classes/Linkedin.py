import requests
import json

class Linkedin():
	def search_persona(self, first_name, second_name):
		url="https://sv.linkedin.com/search/results/people/?firstName="+first_name+"&lastName="+second_name+"&origin=SEO_PSERP"
		r=requests.get(url, cookies={"li_at":"AQEDARNUGNAFid_LAAABbaqba2kAAAFtzqfvaU0AV4sApXLTAUBvo1w-8fekRW6ofs0cQ5XT9PEhNthwjAAOJCbsaG0-F0u5NHz1CIXm5x5ihQxycah3HhZNkvGfDCgC_fuiOwgBCkrAlOJSeuDaQlw4;"})
		for code in r.content.decode().split('<code'):
			if("FIRST_STRONG" in code):
				return json.loads("\n".join(code.split("\n")[1:]).split("</code")[0].replace("&quot;", '"'))
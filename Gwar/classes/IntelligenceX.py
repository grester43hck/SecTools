import requests
import json

class IntelligenceX():
	def search_email(self, q):

		res=[]
		r = requests.post("https://api.intelx.io/intelligent/search",headers={"x-key": "44e3fc83-a89d-48fa-9cac-4d0365e1ace4"},data='{"term":"'+q+'","lookuplevel":0,"maxresults":1000,"timeout":null,"datefrom":"","dateto":"","sort":2,"media":0,"terminate":["a863e8c4-0f9a-4a6e-842e-4493bca14927"]}')
		aux_id = json.loads(r.content.decode())["id"]
		r = requests.get("https://api.intelx.io/intelligent/search/result?id="+aux_id+"&statistics=1",headers={"x-key": "44e3fc83-a89d-48fa-9cac-4d0365e1ace4"})
		for r in json.loads(r.content.decode())["records"]:
			print("[IntelligenceX] Found intelligence ==> ["+r["bucketh"] + "] "+ r["name"])
			storage_id=r["storageid"]
			url = "https://api.intelx.io/file/view?f=0&storageid="+storage_id+"&bucket="+r["bucket"]+"&k=44e3fc83-a89d-48fa-9cac-4d0365e1ace4&license=public"
			req = requests.get(url,headers={"x-key": "44e3fc83-a89d-48fa-9cac-4d0365e1ace4"})
			try:
				password = req.content.decode().split(q)[1].split("\r\n")[0]
			except:
				password = "????"
			res.append((r["bucketh"], q+str(password)))

		return res

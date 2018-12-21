# -*- coding: utf-8 -*-
import requests
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("dll_name", help="DLL name as kernel32.dll (case insensitive)")
parser.add_argument("--functions", help="print functions exported by the library", action='store_true')
args = parser.parse_args()

def req(url):
	r = requests.get(url)
	if (r.status_code==200):
		return r.text.encode("utf-8")
	else:
		return ""

def w10dll_nirsoft_net(dll, func=False):
	dll = dll.replace(".", "_")
	info = req("http://windows10dll.nirsoft.net/"+dll.lower()+".html")
	try:
		desc= info.split("td>")[5].split(" &nbsp")[0].encode()
	except:
		desc= ""
	if(func):
		try:
			func_list= "EXPORTED FUNCION LIST:\n\r "+"\n\r".join(info.split("Exported Functions List")[1].split("</table>")[0].split("<td>")[1:]).replace("\r\n", "").replace("<tr>", "")
		except:
			func_list= ""
	else:
		func_list=""
	return [desc, func_list]
def process_library_com(dll):
	dll=dll.lower()
	aux = req("https://www.google.com/search?q="+dll+"+www.processlibrary.com")
	aux = aux.split("https://www.processlibrary.com")[1].split("&amp;")[0]
	content = req("https://www.processlibrary.com"+aux)
	try:
		desc = [content.split('class="seven columns"')[1].split("<p>")[2].split("</p>")[0]]
	except:
		desc=[]
	return desc

def get_info(dll_name, show_exported_functions):
	info = []
	info+=process_library_com(dll_name)
	info+=w10dll_nirsoft_net(dll_name, show_exported_functions)
	return info

print "Getting the info.."
infos = get_info(args.dll_name, args.functions)
print "<<<<< " + args.dll_name + " INFORMATION >>>>>"
for info in infos:
	if info!="":
		print "[+] -> " + str(info)

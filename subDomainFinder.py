#!/bin/python

import requests
import sys
#import socket
import dns.resolver
import json

def find_subdomains(domain):
	subdomain_list = list()

	##SEARCH findsubdomains.com
	data = requests.get("http://findsubdomains.com/subdomains-of/"+domain)
	links = data.text.split('href="')
	for l in links:
		aux_l = l.split('"')[0]
		if(domain in aux_l and "/" not in aux_l):
			subdomain_list.append(aux_l)

	##SEARCH certspotter.com
	data = requests.get("https://certspotter.com/api/v0/certs?domain="+domain)
	for d in json.loads(data.text):
		for dns in d["dns_names"]:
			if(dns not in subdomain_list):
				subdomain_list.append(dns.encode())

	##hackertarget.com
	data = requests.post("https://hackertarget.com/find-dns-host-records/", data={"theinput":domain,"thetest":"hostsearch","name_of_nonce_field":"76c348276a","_wp_http_referer":"%2Ffind-dns-host-records%2F"})
	domains = data.text.split('<pre id="formResponse">')[1].split("</pre>")[0].split("\n")
	for d in domains:
		if(d.split(",")[0] not in subdomain_list and d.split(",")[0]!=""):
			subdomain_list.append(d.split(",")[0].encode())

	##RETURN RESULTS
	if(len(subdomain_list)>0):
		print("[+] Found " + str(len(subdomain_list)) + " subdomains")		
	return subdomain_list


def dig_subdomains(subdomains):
	ips={}
	for sub in subdomains:
		try:
			for rdata in dns.resolver.query(sub, 'A') :
				try:
	    				ips[str(rdata)].append(sub.encode())
				except KeyError: 
					try:
						a=len(ips[str(rdata)])
					except KeyError:
						ips[str(rdata)]=[sub.encode()]
		except:
			pass

	return ips


def dnsreverselookup(ips):
	other_subdomains={}
	for key in ips:
		data = requests.get("https://www.bing.com/search?q=ip%3A"+key)
		for href in data.text.split('<cite>')[1:]:
			try:
				other_subdomains[key].append(href.replace("https://", "").replace("http://", "").split("/")[0].replace("<", "").encode('utf-8'))
			except KeyError:
				try:
					a = len(other_subdomains[key])
				except KeyError:
					other_subdomains[key]=[href.split("/")[0].encode('utf-8')]


	return other_subdomains
		

if(len(sys.argv)<1):
	print("USAGE: " + argv[0] + " {domain}")
	sys.exit()

subdomains = find_subdomains(sys.argv[1])
ips = dig_subdomains(subdomains)
reverse = dnsreverselookup(ips)

#PRINT INFO
print ("#####################")
print ("Main subdomain list:")
print ("#####################")
for dom in subdomains:
	print ("[+] " + dom)

print ("#####################")
print ("Subdomain by ip")
print ("#####################")
for key in ips:
	print("[+] " + key + ": " + ", ".join(ips[key]))

print ("#####################")
print ("Reverse lookup ip")
print ("#####################")
for key in reverse:
	print("[+] " + key + ": " + ", ".join(reverse[key]))

import sys
import itertools
import hashlib
import argparse


parser = argparse.ArgumentParser(description='Hash formula identificator')
parser.add_argument('--wordlist', dest='wordlist',help='wordlist of possible components of the hash (salt, password, name, phone...)', required=True)
parser.add_argument('--hash', dest='hash',help='hash wich formula we need to identify', required=True)
parser.add_argument('--crypto', default="md5", required=False, dest='crypto',help='Wich cryto to use (supported: md5, sha1)')

args = parser.parse_args()
def generateHash(string, crypto):
	m = hashlib.md5()
	if(crypto=="sha1"):
		m = hashlib.sha1()
	m.update(string)
	return m.hexdigest().encode("utf-8")

def crack(wordlist, hash, crypto):
	with open(wordlist) as f:
		content = f.readlines()
	wordlist = [x.strip() for x in content]
	wordlist=wordlist+wordlist

	real = hash

	print "USING WORDLIST: " + ", ".join(wordlist)

	glues = ["", "-", ".", "_", ":", ";", ",", " "]

	for glue in glues:
		for w_len in range(1,len(wordlist)+1):
			for it in list(itertools.permutations(wordlist, w_len)):
				print ("[-] TRY: "+glue.join(it))
				res = generateHash(glue.join(it), crypto)
				print (res)
				if(res.upper()==real.upper()):
					print ("[+] FOUND! (" + glue.join(it) + ")")
					sys.exit()

crack(args.wordlist, args.hash, args.crypto)
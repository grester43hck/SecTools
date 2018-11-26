from scipy import misc
import numpy as np
from random import randint
import sys 
import argparse
import binascii

parser = argparse.ArgumentParser(description='Recover data hidden in images')
parser.add_argument('-i',help="Input image", required=True)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-o',help="File to put the hidden data in")
group.add_argument('-m',action="store_true", help="Use this if hidden data is a plain text message")
args = parser.parse_args()

crafted_img = args.i

img_data = misc.imread(crafted_img)
length = 0
aux_content=""
content=""
for d in img_data:
	for rgb in d:
		r,g,b = rgb
		if(int(b)%2==0):
			#print str(rgb)
			length+=1
			if(int(r)%2==0): aux_content+="1"
			else: aux_content+="0"
			#print aux_content
if(args.m):
	print binascii.unhexlify('%x' % int("0b"+str(aux_content),2))
else:
	try:
		file = open(args.o,"wb") 
		file.write(binascii.unhexlify('%x' % int("0b"+str(aux_content),2)).decode("hex"))
		file.close()
	except:
		file = open(args.o,"wb") 
		file.write(binascii.unhexlify('%x' % int("0b"+str(aux_content),2)))
		file.close()


from scipy import misc
import numpy as np
from random import randint
import sys
import argparse
import binascii

#ARGUMENTS
parser = argparse.ArgumentParser(description='Hide data into images')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-m',help="Message to hide")
group.add_argument('-f',help="Path to file to hide")
parser.add_argument('-i',help="Input image", required=True)
parser.add_argument('-o',help="Output image", default="out.png")
parser.add_argument("--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("--visible", help="makes output image to be just black where the message would go in a real case (Doesn't encrypt the data in it)",
                    action="store_true")
args = parser.parse_args()

if(args.m==None):	
	print ("[+] Using file hex as message! ")
	print "---------------"
	with open(args.f, 'r') as myfile:
		message = myfile.read()
	message=binascii.hexlify(message)
else: message = args.m

message = list(message)

original_img = args.i
crafted_img = args.o

def letter_to_bin(letter):
	if(isinstance(letter, int)): bin(letter)[2:].zfill(8)
	else:return bin(ord(letter))[2:].zfill(8)

def crypt_data(img_data, pixel_num, message, msg_len, verbose=False, visible=False):
	#CALCS AND INFO	
	full_msg_bin = ""
	for letter in message:
		full_msg_bin+=letter_to_bin(letter)
	if(verbose):print str(full_msg_bin)
	shape = img_data.shape
	rgb_data_number = shape[0]*shape[1]
	if(verbose): print "Number of placeholders: " + str(rgb_data_number)
	if(verbose): print "Number of bites: "+str(len(full_msg_bin))
	if(rgb_data_number<len(full_msg_bin)): 
		print "Image not large enough"
		sys.exit()
	
	#PADDING left
	pad_left = (rgb_data_number-len(full_msg_bin))/2
	pad_right = pad_left+(rgb_data_number-len(full_msg_bin))%2
	for i in range(pad_left):
		before = img_data[int(i/shape[1]), int(i%shape[1])]
		if(verbose):print "Before: "+str(before)
		r=before[0]
		g=before[1]
		b=before[2]
		if(b%2==0): b-=1#BLUE IN PADDING MUST BE ODD
		if(b<0):b=1 #FIX IF b was 0
		img_data[int(i/shape[1]), int(i%shape[1])] = [r,g,b]
		if(verbose):print "content: Padding left"
		if(verbose):print "After: "+str(img_data[int(i/shape[1]), int(i%shape[1])])
		if(verbose):print "----------------_"

	#PAYLOAD
	msg_pointer = 0
	for i in range(pad_left, pad_left+len(full_msg_bin)):
		before = img_data[int(i/shape[1]), int(i%shape[1])]
		if(verbose):print "Before: "+str(before)
		r=before[0]
		g=before[1]
		b=before[2]
		if(b%2==1): b+=1#BLUE IN CONTENT MUST BE EVEN
		if(b>255): b=254#FIX if b was 255 at start
		if(full_msg_bin[msg_pointer]=="1" and r%2==1): r+=1#IF PAYLOAD=1 RED MUST BE EVEN  
		if(r>255): r=254 #FIX if r was 255 at start
		if(full_msg_bin[msg_pointer]=="0" and r%2==0): r+=1#IF PAYLOAD=1 RED MUST BE EVEN  
		if(r>255): r=254 #FIX if r was 255 at start
		if(visible): img_data[int(i/shape[1]), int(i%shape[1])] = [0,0,0]
		else: img_data[int(i/shape[1]), int(i%shape[1])] = [r,g,b]
		if(verbose):print "content: "+full_msg_bin[msg_pointer]
		if(verbose):print "After: "+str(img_data[int(i/shape[1]), int(i%shape[1])])
		if(verbose):print "----------------_"
		msg_pointer+=1

	#PADDING right
	for i in range(pad_left+len(full_msg_bin), pad_left+len(full_msg_bin)+pad_right):
		before = img_data[int(i/shape[1]), int(i%shape[1])]
		if(verbose):print "Before: "+str(before)
		r=before[0]
		g=before[1]
		b=before[2]
		if(b%2==0): b-=1#RED IN PADDING MUST BE ODD
		if(b<0):b=1 #FIX IF b was 0
		img_data[int(i/shape[1]), int(i%shape[1])] = [r,g,b]
		if(verbose):print "content: Padding right"
		if(verbose):print "After: "+str(img_data[int(i/shape[1]), int(i%shape[1])])
		if(verbose):print "----------------_"

	return img_data

#GET ORIGINAL IMG DATA
img_data = misc.imread(original_img)
pixel_num = img_data.shape[0]*img_data.shape[1]
original_shape = img_data.shape

print "[i] Image size: "+str(original_shape[0])+"x"+str(original_shape[1])
print "[i] Pixel number: "+str(pixel_num)
print "---------------"
print "[i] Content length: "+str(len(message))
print "---------------"
img_data = crypt_data(img_data, pixel_num, message, len(message), args.verbose, args.visible)


#craft out image
misc.imsave(crafted_img, img_data)
print "[+] Image saved as "+str(crafted_img)+"!"

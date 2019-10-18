import sys

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()

'''
0 = O 
1 = I or L
2 = Z 
3 = E
4 = h or A
5 = S
6 = b or G
7 = T or j
8 = B or X
9 = g or J
'''


def leet(w):
	traslator = {
	"O":"0",
	"I":"1",
	"L":"1",
	"Z":"2",
	"E":"3",
	"H":"4",
	"A":"4",
	"S":"5",
	"G":"6",
	"T":"7",
	"J":"7",
	"B":"8",
	"X":"8",
	"G":"9",
	"J":"9"
	}

	res=""
	for letter in list(w):
		l = letter
		try:
			l=traslator[letter.upper()]
		except:
			pass
		res+=l
	return res

for line in lines:
	print(leet(line))
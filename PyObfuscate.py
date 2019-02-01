import base64
import argparse
from random import randint


parser = argparse.ArgumentParser(description='Ofuscate python code')
parser.add_argument('--infile', help='file to ofuscate code', required=True)
parser.add_argument('--crypt', help='XOR code', action="store_true")
args = parser.parse_args()

def obfuscate(code, secret_char, crypt):
    if(crypt): c = ' '.join(str(ord(x)^ord(secret_char)) for x in str(code))
    else: c = ' '.join(str(ord(x)) for x in str(code))
    c = base64.b64encode(c)
    return c

secret_char =chr(randint(40, 200)) 

with open(args.infile, 'r') as myfile:
    c=myfile.read()

result = "import base64;c='''"+obfuscate(c, secret_char, args.crypt)+"''';"
if(args.crypt): result += "exec(''.join(chr(int(x)^ord('"+secret_char+"')) for x in base64.b64decode(c).split()))"
else: result += "exec(''.join(chr(int(x)) for x in base64.b64decode(c).split()))"
print result

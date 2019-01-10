from scapy.all import *
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--ip', help='filter traffic by ip')
parser.add_argument('--decrypt', action='store_true', help='Try to parse hex traffic to ascii')

args = parser.parse_args()

ALL_IP = True
ip_whitelist=[]
if(args.ip!=None):
	ip_whitelist.append(args.ip)
	ALL_IP=False
DECRYPT = args.decrypt

print "CONFIG"
print "ALL_IP: "+str(ALL_IP)
print "IP FILTER: "+str(ip_whitelist)
print "DECRYPT: "+str(DECRYPT)

class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

def expand(x):
    yield x
    while x.payload:
        x = x.payload
        yield x

def pkt_callback(pkt):
    if(pkt[IP].dst in ip_whitelist or ALL_IP):
	try:
		print( bcolors.OKGREEN +"["+str(pkt[IP].sport)+"-->"+str(pkt[IP].dport)+"]"+pkt[Raw].load.encode("hex") + (" ---- \n\r"+bcolors.ENDC+pkt[Raw].load if DECRYPT else "")) 
	except IndexError:
		print(bcolors.OKGREEN +"["+str(pkt[IP].sport)+"-->"+str(pkt[IP].dport)+"]" + " empty")
    if(pkt[IP].src in ip_whitelist):
	try:
		print( bcolors.OKBLUE +"["+str(pkt[IP].dport)+"<--"+str(pkt[IP].sport)+"]"+pkt[Raw].load.encode("hex") + (" ---- \n\r"+bcolors.ENDC+pkt[Raw].load if DECRYPT else "")) 
	except IndexError:
		print(bcolors.OKBLUE +"["+str(pkt[IP].dport)+"<--"+str(pkt[IP].sport)+"]" + " empty")

sniff(iface="eth0", prn=pkt_callback, filter="tcp", store=0)

from scapy.all import *
import argparse
import netifaces as ni

##ARG PARSER
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--ip', help='filter traffic by ip')
parser.add_argument('--decrypt', action='store_true', help='Try to parse hex traffic to ascii')
parser.add_argument('--all', action='store_true', help='Show empty (0 len payload) pakets')
parser.add_argument('--interface', default="eth0", help='Interface')
args = parser.parse_args()

##VARS
ALL_IP = True
ip_whitelist=[]
if(args.ip!=None):
	ip_whitelist.append(args.ip)
	ALL_IP=False
DECRYPT = args.decrypt
SHOW_ALL = args.all
INTERFACE = args.interface
ni.ifaddresses(INTERFACE)
LOCAL_IP = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']

##PRINT CONFIG
print ("--- CONFIG ---")
print ("[+] INTERFACE: \t"+str(INTERFACE) + "("+LOCAL_IP+")")
print ("[+] ALL_IP: \t\t"+str(ALL_IP))
print ("[+] IP FILTER: \t"+(str(ip_whitelist) if len(ip_whitelist)>0 else "ALL"))
print ("[+] DECRYPT: \t\t"+str(DECRYPT))

##CLASSES AND METHODS
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
	if(pkt[IP].dst in ip_whitelist or (ALL_IP and pkt[IP].src == LOCAL_IP)):
		try:
			print( bcolors.OKGREEN +"["+str(pkt[IP].src)+":"+str(pkt[IP].sport)+"-->"+str(pkt[IP].dst)+":"+str(pkt[IP].dport)+"]"+pkt[Raw].load.encode("hex") + (" ---- \n\r"+bcolors.ENDC+pkt[Raw].load.encode("latin1") if DECRYPT else "")) 
		except UnicodeDecodeError:
			print( bcolors.OKGREEN +"["+str(pkt[IP].src)+":"+str(pkt[IP].sport)+"-->"+str(pkt[IP].dst)+":"+str(pkt[IP].dport)+"]"+pkt[Raw].load.encode("hex") + " ---- "+bcolors.ENDC+"CRYPTED") 
		except IndexError:
			if(SHOW_ALL): print(bcolors.OKGREEN +"["+str(pkt[IP].src)+":"+str(pkt[IP].sport)+"-->"+str(pkt[IP].dst)+":"+str(pkt[IP].dport)+"]" + " empty")
	if(pkt[IP].src in ip_whitelist or (ALL_IP and pkt[IP].dst == LOCAL_IP)):
		try:
			print( bcolors.OKBLUE +"["+str(pkt[IP].dst)+":"+str(pkt[IP].dport)+"<--"+str(pkt[IP].src)+":"+str(pkt[IP].sport)+"]"+pkt[Raw].load.encode("hex") + " ---- \n\r"+bcolors.ENDC+pkt[Raw].load.encode("latin1")) 
		except UnicodeDecodeError:
			print( bcolors.OKBLUE +"["+str(pkt[IP].dst)+":"+str(pkt[IP].dport)+"<--"+str(pkt[IP].src)+":"+str(pkt[IP].sport)+"]"+pkt[Raw].load.encode("hex") + " ---- "+bcolors.ENDC+"CRYPTED") 
		except IndexError:
			if(SHOW_ALL): print(bcolors.OKBLUE +"["+str(pkt[IP].dst)+":"+str(pkt[IP].dport)+"<--"+str(pkt[IP].src)+":"+str(pkt[IP].sport)+"]" + " empty")

##MAIN CODE
sniff(iface="eth0", prn=pkt_callback, filter="tcp", store=0)

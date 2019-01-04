import pika
import argparse

#GLOBAL VARS
msg = 'ANYONE LISTENS?'
mqrabbit_host = "localhost"

#METHODS

#ARG PARSER
parser = argparse.ArgumentParser()
parser.add_argument("--dict", help="dictionary of channels to search for")
parser.add_argument("--host", help="rabbitMQ host ip")
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()

mqrabbit_host = args.host

##GET WORD LIST FROM DICT
with open(args.dict) as f:
	word_list = f.readlines()
word_list = [x.strip() for x in word_list] ##FIX WORD LIST END LINES

#SEND 2 MESSAGES TO EVERY CHANNEL IN LIST
connection = pika.BlockingConnection(pika.ConnectionParameters(mqrabbit_host))
channel = connection.channel()
if(args.verbose): print "[+] STAGE 1: Sending all messages..."
for word in word_list:
	channel.queue_declare(queue=word)
	if(args.verbose): print "[-] Sending messages to channel: "+str(word)
	for i in range(2):
		if(args.verbose): print "[-] Sending message "+str(i)
		channel.basic_publish(exchange='', routing_key=word, body=msg)

#RETRIEVE 2 MESSAGES FROM EVERY CHANNEL IN LIST
if(args.verbose): print "[+] STAGE 2: Recovering messages.."
for word in word_list:
	valid = False
	channel.queue_declare(queue=word)
	if(args.verbose): print "[-] Sending messages to channel: "+str(word)
	for i in range(2):
		if(args.verbose): print "[-] Retrieving back message "+str(i)
		try:
			method, prop, body = channel.basic_get(queue=word, no_ack=True)
			if(method==None and prop==None and body==None): valid = True
		except pika.exceptions.ChannelClosed:
			print "ChannelClosed error..."
	if(valid): print "[!] FOUND ACTIVE CHANNEL: " +str(word)
connection.close()

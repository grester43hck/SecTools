import sys; sys.__stdout__ = sys.stdout
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import hashlib
import unicodedata, re
import argparse
import threading
import socket
import datetime

class Crypter:

	##INIT
	def __init__(self, conf={}, verbose=False):
		self.conf=conf
		self.verbose=verbose

	##AUX FUNCTIONS
	def remove_unprintable(self, data):
		all_chars = (chr(i) for i in range(sys.maxunicode))
		control_chars = ''.join(c for c in all_chars if unicodedata.category(c) == 'Cc')
		control_char_re = re.compile('[%s]' % re.escape(control_chars))
		return control_char_re.sub('', data)

	def pad(self, s, bs):
		return str(s) + (bs - len(s) % bs) * chr(bs - len(s) % bs)

	def aes_b64(self, data, key, crypt=True):
		self.aes_iv = 0
		self.aes_key = key[:32]
		backend = default_backend()
		cipher = Cipher(algorithms.AES(self.aes_key.encode('ascii')), modes.CBC(str("A"*(16-len(str(self.aes_iv)))+str(self.aes_iv)).encode('ascii')), backend=backend)
		if(crypt):
			encryptor = cipher.encryptor()
			cipher_text = encryptor.update(self.pad(data,32).encode('ascii')) + encryptor.finalize()
			return base64.b64encode(cipher_text).decode()
		else:
			aux = base64.b64decode(data)
			decryptor = cipher.decryptor()
			plain_text = decryptor.update(aux) + decryptor.finalize()
			return self.remove_unprintable(plain_text.decode("utf-8"))

	##MAIN FUNCTIONS
	def crypt(self, data, GUI):
		aux_data=data
		for key, val in self.conf.items():
			GUI.add_debug("[+] Crypter |_> Applying "+str(key) + " cipher...")
			aux_data = val["fun"](self, aux_data, val["key"], True)
			if(self.verbose): GUI.add_debug("[+] Crypter |____> Result: " + aux_data)
		return aux_data

	def decrypt(self, data, GUI):
		aux_data=data
		for key in reversed(list(self.conf.keys())):
			GUI.add_debug("[+] Crypter |_> Applying "+str(key) + " decipher...")
			aux_data = self.conf[key]["fun"](self, aux_data, self.conf[key]["key"], False)
			if(self.verbose): GUI.add_debug("[+] Crypter |_______> Result: " + aux_data)
		return aux_data

class Connection:

	buff=[]

	def __init__(self, cipherSuite, ip, port, GUI, server=True):
		self.GUI=GUI
		self.cipherSuite=cipherSuite
		self.ip=ip
		self.port=port
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if(server):
			self.serve()
		else:
			self.connect()


	def cipher(self, data, GUI):
		return self.cipherSuite.crypt(data, GUI)

	def decipher(self, data, GUI):
		return self.cipherSuite.decrypt(data, GUI)

	def serve(self):
		#act as server
		self.conn.bind((self.ip, self.port))
		self.conn.listen(1)
		print("[+] Connector --> listening on "+str(self.ip)+":"+str(self.port))
		self.conn, self.remo_addr = self.conn.accept()
		print("[+] Connector --> Got connexion from "+str(self.remo_addr))
		
		#LANZA HILO PARA LA RECEPCION DE DATOS
		recv_thread = threading.Thread(target=self.read)
		recv_thread.setDaemon(True)
		recv_thread.start()

	def connect(self):
		print("[+] Connector --> Connecting with "+str(self.ip) + ":" + str(self.port))
		self.conn.connect((self.ip, self.port))
		print("[+] Connector --> Connected.")

		#LANZA HILO PARA LA RECEPCION DE DATOS
		recv_thread = threading.Thread(target=self.read)
		recv_thread.setDaemon(True)
		recv_thread.start()

	def read(self):
		#read msg
		while(True):
			data = self.conn.recv(1024)
			#if data != "":
			self.buff.append("Recv>> "+str(self.decipher(data.decode("utf-8"), self.GUI)+"\n"))
			self.GUI.update_message_board(self.buff[-10:])

	def send(self, data):
		self.buff.append("Sent>> "+str(data))
		msg = self.cipher(data, self.GUI)
		self.conn.send(msg.encode())
		self.GUI.update_message_board(self.buff[-10:])

##USER INTERFACE
from tkinter import *
class MyFirstGUI:

	debug_buff=[]

	def __init__(self, master, args, cipherSuite):

		self.cipherSuite = cipherSuite
		self.conn = Connection(cipherSuite, args.ip, int(args.port), self, args.server)

		self.master = master
		master.title("Ultra secure Chat")

		self.msgboard_label = Label(master, text="Message board")
		self.msgboard_label.pack()

		self.message_board = Label(master, text="")
		self.message_board.pack()

		self.txt = Entry(master,width=100)
		self.txt.pack()

		self.greet_button = Button(master, text="Send>>", command=self.send)
		self.greet_button.pack()

		self.close_button = Button(master, text="Close", command=master.quit)
		self.close_button.pack()

		self.debugboard_label = Label(master, text="Debug board")
		self.debugboard_label.pack()

		self.debugboard = Label(master, text="")
		self.debugboard.pack()

	def send(self):
		print("Send button pressed!"+self.txt.get())
		self.conn.send(self.txt.get())
		self.txt.delete(0, len(self.txt.get()))

	def add_debug(self, msg):
		self.debug_buff.append(str(datetime.datetime.now())+str(msg))
		self.debugboard["text"]="\n".join(self.debug_buff[-10:])

	def update_message_board(self, messages):
		self.message_board["text"]="\n".join(messages)


##INDEPENDENT CRYPTO FUNCTIONS
def reverse_crypt(data, key, crypt=True):
	return data[::-1]

def obfuscate_crypt(data, key, crypt=True):
	if(crypt):
		return data.replace("=", "%")
	else:
		return data.replace("%", "=")

##MAIN CODE
parser = argparse.ArgumentParser(description='Ultra secure chat')
parser.add_argument('ip', metavar='ip', help='ip')
parser.add_argument('port', metavar='port', help='port')
parser.add_argument('--server', action='store_true')
parser.add_argument('--verbose', action='store_true')
args = parser.parse_args()

cipherSuite = Crypter(conf={
	"AES_b64": {
		"fun": lambda self, data, key, crypt: self.aes_b64(data, key, crypt),
		"key": ""
	},
	"AES_b64_2": {
		"fun": lambda self, data, key, crypt: self.aes_b64(data, key, crypt),
		"key": ""
	},
	"AES_b64_3": {
		"fun": lambda self, data, key, crypt: self.aes_b64(data, key, crypt),
		"key": ""
	},
	"AES_b64_4": {
		"fun": lambda self, data, key, crypt: self.aes_b64(data, key, crypt),
		"key": ""
	},
	"AES_b64_5": {
		"fun": lambda self, data, key, crypt: self.aes_b64(data, key, crypt),
		"key": "bertberthbertbergnbercxgvwenbrethvcewrtxbrefgbevtchynbexbafsbvtyehnvxgc"
	},
	"Reverse": {
		"fun": lambda self, data, key, crypt: reverse_crypt(data, key, crypt),
		"key": ""
	},
	"Obfuscate": {
		"fun": lambda self, data, key, crypt: obfuscate_crypt(data, key, crypt),
		"key": ""
	}
	}, verbose=args.verbose)

root = Tk()
my_gui = MyFirstGUI(root, args, cipherSuite)
root.mainloop()

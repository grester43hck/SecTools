import sys
import time
from colorama import init
init()
import operator

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class trafficAnalyzer():
	original_lines=[]
	rule=[]

	def str_to_hex(self,str):
		return [str[i:i+2] for i in range(0, len(str), 2)]

	def load_file(self,file):
		with open(file) as f:
			self.original_lines=[line.strip() for line in f]

	def pretty_rule(self):
		aux=[]
		for x in self.rule:
			if(x=="="): aux.append(bcolors.OKGREEN+x)
			if(x=="v"): aux.append(bcolors.FAIL+x)
			if(x=="^"): aux.append(bcolors.OKBLUE+x)
			if(x=="$"): aux.append(bcolors.WARNING+x)
			if(x=="C"): aux.append(bcolors.ENDC+x)
		print (bcolors.ENDC+"[+++]"+" ".join(aux))

	def pretty_samples(self):
		for l in self.original_lines:
			aux=[]
			for x in range(0,len(self.rule)): 
				if(self.rule[x]=="="): aux.append(bcolors.OKGREEN+self.str_to_hex(l)[x])
				if(self.rule[x]=="v"): aux.append(bcolors.FAIL+self.str_to_hex(l)[x])
				if(self.rule[x]=="^"): aux.append(bcolors.OKBLUE+self.str_to_hex(l)[x])
				if(self.rule[x]=="$"): aux.append(bcolors.WARNING+self.str_to_hex(l)[x])
				if(self.rule[x]=="C"): aux.append(bcolors.ENDC+self.str_to_hex(l)[x])
			print (bcolors.ENDC+"[+++]"+"".join(aux))

	def generate_rule(self):
		self.rule = [None for x in range(int(len(self.original_lines[0])/2))]
		for i in range(1,len(self.original_lines)):
			line1=self.str_to_hex(self.original_lines[i-1])
			line2=self.str_to_hex(self.original_lines[i])
			for j in range(0, len(line1)):
				if(line1[j]==line2[j] and self.rule[j]==None): self.rule[j]="="
				if(line1[j]>line2[j] and self.rule[j]!="^" and self.rule[j]!="$"): self.rule[j]="v"
				if(line1[j]>line2[j] and self.rule[j]=="^"): self.rule[j]="$"
				if(line1[j]<line2[j] and self.rule[j]!="v" and self.rule[j]!="$"): self.rule[j]="^"
				if(line1[j]<line2[j] and self.rule[j]=="v"): self.rule[j]="$"

	def get_best_control_option(self, data):
		aux_data = list(set(data))
		aux_diff=[]
		order = []
		for j in range(0, len(aux_data)):
			indexes = [i for i, x in enumerate(data) if x == aux_data[j]]
			order.append(indexes[0])
			if(len(indexes)>len(data)*0.1 and len(indexes)>3):
				diffs=[]
				for a in range(1, len(indexes)):
					diffs.append(indexes[a]-indexes[a-1])
				aux_diff.append(max(diffs)-min(diffs))
			else:
				aux_diff.append(10)
		ind = aux_diff.index(min(aux_diff))
		return data[order[ind]]

	def generate_controls(self):
		rule_set=[]
		aux=self.rule[0]
		##RULE_SET GENERATION
		for x in range(1,len(self.rule)):
			if(self.rule[x-1]==self.rule[x]):
				aux+=self.rule[x]
			else:
				rule_set.append(aux)
				aux=self.rule[x]
		rule_set.append(aux)

		##PACK DATA BASED ON RULE_SET
		#for x in range(0, len(self.original_lines)):
		aux = self.str_to_hex(self.original_lines[0])
		cont=0
		for r in rule_set:
			data = aux[cont:cont+len(r)]
			if(len(data)>4):
				delimiter = self.get_best_control_option(data)
				indexes = [i for i, x in enumerate(data) if x == delimiter]
				if(len(indexes)>len(data)*0.1 and len(indexes)>1):
					for i in indexes:
						self.rule[cont+i]="C"
			cont+=len(r)

	def analyze(self, file):
		print (bcolors.ENDC+"[+] Loading data...")
		self.load_file(file)
		print (bcolors.ENDC+"[+] Generating rule...")
		self.generate_rule()
		print (bcolors.ENDC+"[+] Guessed rule:")
		self.pretty_rule()
		print (bcolors.ENDC+"[+] Rule applied to few samples:")
		self.pretty_samples()
		print (bcolors.ENDC+"[+] Guessing control structures...")
		self.generate_controls()
		print (bcolors.ENDC+"[+] Guessed rule:")
		self.pretty_rule()
		print (bcolors.ENDC+"[+] Rule applied to few samples:")
		self.pretty_samples()


TA = trafficAnalyzer()
TA.analyze(sys.argv[1])

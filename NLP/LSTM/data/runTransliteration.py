# -*- coding: utf-8 -*-
import csv
import sys
import os
reader = csv.reader(open('svar.csv', 'r'))
vowels = {}
for row in reader:
	k, v = row
	vowels[k] = v

reader = csv.reader(open('vyanjan.csv', 'r'))
consonants = {}
for row in reader:
	k, v = row
	consonants[k] = v


def convert_file(content):

	
	
	

	str1 = ""

	for y in content.split(" "):
		for i in range(len(y)):
			if (i+1<len(y) and y[i+1].strip()==' ़'.strip()):
				c = y[i]+y[i+1]
				p=2
			else:
				c = y[i]
				p=1
			if (c in vowels.keys()):
				str1 = str1 + vowels[c]
			elif (c in consonants.keys()):
				if(i+p<len(y) and y[i+p] in consonants.keys()):
					if ((c=='झ' and i!=0) or (i!=0 and i+p+1<len(y) and y[i+p+1] in vowels.keys())): # add 'a' after 'jh', only if झ appears in the starting of the word
						str1 = str1 + consonants[c]
					else:
						str1 = str1 + consonants[c]+'a'
				else:
					str1 = str1 + consonants[c]
			elif y[i] in ['\n','\t',' ','!',',','।','-',':','\\','_','?'] or c.isalnum():
				str1 = str1 + c.replace('।','.')
		str1 = str1 + " "
	return str1
	# output_folder = "/Users/tanweersalah/Desktop/University/Machine learning/GenAI/NLP/LSTM/data/output"
	# output_file = os.path.join(output_folder,hindi_file.split('/')[-1])
	
	# file = open(output_file ,'w')
	# file.write(str1.strip())
	# file.close()
	# print(output_file+" OUTPUT")

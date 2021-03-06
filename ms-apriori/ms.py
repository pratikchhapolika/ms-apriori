import sys
import csv
import re
from collections import OrderedDict
import itertools
import copy
import os

transactions = []
cannot_be_together = []
sdc = 0.0
everything = {}
must_haves = []
f1_count = {}
fis_final = []

# Read and parse input file and store each t to transactions, add each item to everything if unique and update support count
def read_input(input_location):
	# Open input_location and parse line by line
	input_file = open(input_location, "r")
	for mindex, m in enumerate(input_file):
		# Find all ints, put into a list, then append them to list_of_items
		m = m.replace('\n', '')
		m = m.replace('{', '')
		m = m.replace('}', '')
		m = m.split(', ')
		# m = list(map(int, m))
		transactions.append(m)
		for i in m:
			if i not in everything.keys():
				everything.update({i: [1]})
			else:
				everything[i][0] += 1
	global f1_count
	f1_count = copy.deepcopy(everything)
	# For every unique item in everything, calculate and update support for each item
	for k, v in everything.items():
		v[0] = float(v[0]) / len(transactions)

def sort_everything(everything):
	everything = OrderedDict(sorted(everything.items(), key=lambda t: t[0]))
	everything = [[k,v] for k, v in everything.items()]
	everything.sort(key=lambda pair: pair[1][1])
	init_pass(everything, transactions)

# Read and parse parameter-list and store each value to appropriate lists
def read_parameter(parameter_location):
	parameter_file = open(parameter_location, "r")
	for index, i in enumerate(parameter_file):
		# Parse MIS to mis_dict
		if 'MIS' in i:
			# s = re.findall(r'(\d+)', i)
			# item = int(s[0])
			item = i.split(')')
			mis = re.findall(r'\d+', item[1])
			mis = float(mis[0] + '.' + mis[1])
			#print(mis)
			item = item[0].split('(')[1]
			#print(item)
			# item = s[0]
			# mis = float(s[1] + '.' + s[2])
			global everything
			if item in everything.keys():
				everything[item].append(mis)
		# Parse SDC to sdc
		elif 'SDC' in i:
			s = re.findall(r'\d+\.\d+', i)
			global sdc
			sdc = float(s[0])
		# Parse cannot_be_together to list_of_cbt
		elif 'cannot_be_together' in i:
			# s = re.findall(r'{\d+[, \d+]*}', i)
			# for e in s:
			# 	e = re.findall(r'\d+', e)
			# 	# e = [int(x) for x in e]
			# 	global cannot_be_together
			# 	cannot_be_together.append(e)
			# s = re.findall(r'{.*[, .*]*}', i)
			#print(s)
			# s = s.split(', ')
			#print(cannot_be_together)
			# s = re.findall(r'{.*}+', i)
			i = i.split('cannot_be_together: ')[1]
			i = i.replace('\n', '')
			i = i.split('}, ')
			i = [x.replace('{', '') for x in i]
			i = [x.replace('}', '') for x in i]
			i = [x.split(', ') for x in i]
			for j in i:
				cannot_be_together.append(j)
		# Parse must-have to list_of_mh
		elif 'must-have' in i:
			# s = re.findall(r'\d+', i)
			# s = [int(x) for x in s]
			s = i.replace('must-have: ', '')
			s = s.split(' or ')
			global must_haves
			must_haves = list(s)
			print(must_haves)
	sort_everything(everything)

# First pass to generate seeds L
def init_pass(M, T):
	# Generate empty seed L
	L = []
	# Store value of minimum MIS for each itemset
	min_mis = 0.0
	for i in M:
	 	# If support >= mis first item, then append to L
	 	if i[1][0] >= i[1][1] and min_mis == 0.0:
	 		min_mis = i[1][1]
	 		L.append(i)
	 		continue
	 	# For every element after first item, append if support >= min_mis
	 	elif min_mis != 0.0:
	 		if i[1][0] >= min_mis:
	 			L.append(i)
	# Generate 1-itemsets using L
	generate_F1_itemsets(L)

# Generate F1 item-sets
def generate_F1_itemsets(L):
	# For each item in L, if support < mis, prune it from L
	temp = []
	for i in L:
		if i[1][0] >= i[1][1]:
			temp.append(i)
	F1 = list(temp)
	# print("F1 before must-haves: " + str(F1))
	# Must_haves check
	if len(must_haves) > 0:
		f_temp = []
		for i in F1:
			if i[0] in must_haves:
				f_temp.append(i[0])
				F1 = list(f_temp)
	else:
		f_temp = []
		for i in F1:
			f_temp.append(i[0])
			F1 = list(f_temp)
	# print("F1: " + str(F1))
	# print(f1_count)
	for i in f1_count:
		if i in F1:
			fis_final.append([i, f1_count.get(i)[0], 0])
	print("FIS 1 final: " + str(fis_final))
	output_patterns = open(r'outputpatterns3.txt', 'w+')
	if len(fis_final) > 0:
		output_patterns.write("Frequent 1-itemsets\n\n")
		for i in fis_final:
			output_patterns.write('\t' + str(i[1]) + ' : ' + '{' + str(i[0]) + '}\n')
		output_patterns.write('\n')
		output_patterns.write('\tTotal number of frequent 1-itemsets = ' + str(len(fis_final)) + '\n')
	output_patterns.close()
	# global fis_final
	# fis_final = []
	# Generate k >= 2 item-sets
	generate_item_sets(L)

# Generate F(k-1) item-sets
def generate_item_sets(L):
	k = 2
	# Declare Fk to hold freq item-sets
	freq_itemsets = []
	# Declare Ck_count to hold candidate c count
	Ck_count = {}
	# Declare Ck_tail_count to hold candidate c tail count
	Ck_tail_count = {}
	# For k=2 or k>=2 and while Fk != empty
	while (k == 2 or len(freq_itemsets) > 0):
		fis_final = []
		# If k == 2, run generate 2-itemsets
		if k == 2:
			print("K=2 candidate gen")
			Ck = L2candidate_gen(L, sdc) # k=2
		else:
			print("K=" + str(k) + " candidate gen")
			Ck = MSCandidate_gen(freq_itemsets, sdc)

		# print("Ck length: " + str(len(Ck)))
		freq_itemsets = []
		# For each transaction t in T
		for t in transactions:
			# For each candidate c in Ck
			for c in Ck:
				# If c is contained in t, increment c.count by 1
				if set(c) <= set(t):
					if str(c) in Ck_count.keys():
						Ck_count[str(c)] += 1
					else:
						Ck_count.update({str(c): 1})
				# If c[1:] is contained in t, increment c[1:].count by 1
				if set(c[1:]) <= set(t):
					# if str(c[1:]) in Ck_tail_count.keys():
					if str(c) in Ck_tail_count.keys():
						# Ck_tail_count[str(c[1:])] += 1
						Ck_tail_count[str(c)] += 1
					else:
						# Ck_tail_count.update({str(c[1:]): 1})
						Ck_tail_count.update({str(c): 1})

		# For each candidate c in Ck, if c.support >= c[0].mis, append to Fk
		for c in Ck:
			if str(c) in Ck_count:
				if float(Ck_count[str(c)]) / len(transactions) >= everything[c[0]][1]:
					freq_itemsets.append(c)
					# print("appended: " + str(c))
				# else:
				 	# print(str(float(Ck_count[str(c)]) / len(transactions)) + " !>= " + str(everything[c[0]][1]))
		# print("Ck_count: " + str(Ck_count))
		# print("Ck_tail_count: " + str(Ck_tail_count))
		freq_itemsets_to_print = []
		# Cannot_be_together checks
		if len(cannot_be_together) > 0:
			temp = []
			for i in freq_itemsets:
				for j in cannot_be_together:
					if not(set(j) <= set(i)):
						temp.append(i)
						break
			freq_itemsets_to_print = list(temp)
		else:
			temp = []
			for i in freq_itemsets:
				temp.append(i)
			freq_itemsets_to_print = list(temp)
		# print("between cbt and mh: " + str(freq_itemsets_to_print))
		# Must_have checks
		if len(must_haves) > 0:
			temp2 = []
			for i in freq_itemsets_to_print:
				for j in must_haves:
					if j in i:
						temp2.append(i)
						# print("appended: " + str(i))
						break
			freq_itemsets_to_print = list(temp2)
		for i in freq_itemsets_to_print:
			fis_final.append([i, Ck_count.get(str(i)), Ck_tail_count.get(str(i))])

		if len(freq_itemsets_to_print) < 1:
			sys.exit(0)
		output_patterns = open(r'outputpatterns3.txt', 'a+')
		output_patterns.write('\nFrequent ' + str(k) + '-itemsets\n\n')
		for i in fis_final:
			inside = ','.join(map(str, i[0]))
			output_patterns.write('\t' + str(i[1]) + ' : ' + '{' + str(inside) + '}\n')
			output_patterns.write('Tail count = ' + str(i[2]) + '\n')
		output_patterns.write('\n' + '\t' + 'Total number of frequent ' + str(k) + '-itemsets = ' + str(len(fis_final)) + '\n')
		output_patterns.close()
		# print("Freq after all for k" + str(k) + ": " + str(freq_itemsets))
		# print("Freq to print for k" + str(k) + ": " + str(freq_itemsets_to_print))
		print("fis_final for : " + str(k) + " : " + str(fis_final))
		# USE COUNT AND C.COUNT TO CHECK TO PRUNE FIS!!!
		k += 1

def L2candidate_gen(L, sdc):
	c2 = []
	for l in range(len(L)):
		l_mis = 0.0
		l_sup = 0.0
		if L[l][1][0] >= L[l][1][1]:
			l_mis = L[l][1][1]
			l_sup = L[l][1][0]
			for h in range(l + 1, len(L)):
				if L[h][1][0] >= l_mis and abs(L[h][1][0] - l_sup) <= sdc:
					c2.append([L[l][0], L[h][0]])
	return c2

def MSCandidate_gen(freq_itemsets, sdc):
	Ck = []
	f1 = []
	f2 = []
	combinations = []
	for i in range(len(freq_itemsets)):
		f1 = freq_itemsets[i][0:-1]
		for j in range(i + 1, len(freq_itemsets)):
			f2 = freq_itemsets[j][0:-1]
			# print(everything[freq_itemsets[i][-1]][0])
			if (f1 == f2) and abs(everything[freq_itemsets[i][-1]][0] - everything[freq_itemsets[i][-1]][0]) <= sdc:
				temp = list(freq_itemsets)
				c1 = list(temp[i])
				c2 = temp[j][-1]
				c1.append(c2)
				Ck.append(c1)

	print("F2: " + str(freq_itemsets))
	# print("Ck before removal: " + str(Ck))

	i = 0
	while i < len(Ck):
		subsets = list(itertools.combinations(Ck[i], len(Ck[i]) - 1))
		for s in subsets:
			s = list(s)
			if (Ck[i][0] in s) or (everything[Ck[i][1]][1] == everything[Ck[i][1]][1]):
				if s not in freq_itemsets:
					# print("removing: " + str(Ck[i]))
					Ck.remove(Ck[i])
		i += 1
	# print("Ck after removal: " + str(Ck))
	return Ck

if len(sys.argv) == 3:
	read_input(str(sys.argv[1]))
	read_parameter(str(sys.argv[2]))
	print("fis_final: " + str(fis_final))
	# for i in range(len(fis_final)):
	# 	output_patterns.write('Frequent ' + str(i + 1) + '-itemsets\n')
	# 	output_patterns.write('\n')
	# 	output_patterns.write('\t' + str(fis_final[i][1]) + ' : ' + str(fis_final[i][0]) + '\n')
else:
	print("Please run as python ms-apriori.py [input_file].txt [parameter_file].txt")
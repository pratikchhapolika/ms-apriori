import sys
import csv
import re

# List of values and their respective MIS values
mis_dict = {}
# List of given transactions
list_of_transactions = []
# List of cannot-be_together sets
list_of_cbt = []
# List of items
list_of_items = []
# List of must-have items
list_of_mh = []
# Support difference constraint (phi)
sdc = 0.0

# Read and parse input file and store each transaction to list_of_transactions
def read_input(input_location):
	# Open input_location and parse line by line
	input_file = open(input_location, "r")
	for mindex, m in enumerate(input_file):
		m = re.findall(r'\d+', m)
		m = list(map(int, m))
		list_of_transactions.append(m)
		for i in m:
			if i not in list_of_items:
				list_of_items.append(i)
	print(list_of_transactions)
	print(list_of_items)

# Read and parse parameter-list and store each value to appropriate lists
def read_parameter(parameter_location):
	parameter_file = open(parameter_location, "r")
	for index, i in enumerate(parameter_file):
		# Parse MIS to list_of_mis
		if 'MIS' in i:
			s = re.findall(r'(\d+)', i)
			item_no = int(s[0])
			mis_value = float(s[1] + '.' + s[2])
			mis_dict.update({item_no: mis_value})
		elif 'SDC' in i:
			s = re.findall(r'\d+\.\d+', i)
			sdc = float(s[0])
		elif 'cannot_be_together' in i:
			s = re.findall(r'{\d+[, \d+]*}', i)
			for e in s:
				e = re.findall(r'\d+', e)
				e = [int(x) for x in e]
				list_of_cbt.append(e)
		elif 'must-have' in i:
			s = re.findall(r'\d+', i)
			s = [int(x) for x in s]
			list_of_mh = s

# Check for command line arguments
if len(sys.argv) == 3:
	read_parameter(str(sys.argv[2]))
	read_input(str(sys.argv[1]))
else:
	print("Please run as python ms-apriori.py [input_file].txt [parameter_file].txt")
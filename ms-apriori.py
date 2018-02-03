import sys
import csv

# List of values and their respective MIS values
list_of_mis = []
# List of given transactions
list_of_transactions = []
# List of items
list_of_items = []
# Support difference constraint (phi)
SDC = 0.0

# Read and parse input file and store each transaction to list_of_transactions
def read_input(input_location):
	# Open input_location and parse line by line
	input_file = open(input_location, "r")
	for mindex, m in enumerate(input_file):
		m = m.replace('{', '')
		m = m.replace('}', '')
		m = m.replace('\n', '')
		temp_set = m.split(', ')
		# temp_set = set(temp_set)
		list_of_transactions.append(temp_set)

# Read and parse parameter-list and store each value to appropriate lists
def read_parameter(parameter_location):
	parameter_file = open(parameter_location, "r")
	for index, i in enumerate(parameter_file):
		# Parse MIS to list_of_mis
		if "MIS" in i:
			i = i[4:-1]
			i = i.split(')')
			item_no = i[0]
			i = str(i)
			i = i.split('=')
			temp_mis = i[1]
			temp_mis = temp_mis.replace('\']', '')
			temp_mis = temp_mis.replace(' ', '')
			list_of_mis.append({item_no: temp_mis})
		# Parse and store SDC
		elif "SDC" in i:
			i = i.split(' = ')
			i = i[1]
			SDC = i
		# Custom arguments
		elif "cannot_be_together" in i:
			# PARSE THIS and STORE
			i = i.split(': ')
			i = str(i)
			i = i.split(', ')
			i = i[1:]
		elif "must-have" in i:
			i = i.split(': ')
			i = i[1]
			i = str(i)
			i = i.replace('\n', '')
			i = i.split(' or ')

# def MS_Apriori(T, MS, SDC):
	

# Check for command line arguments
if len(sys.argv) == 3:
	read_parameter(str(sys.argv[2]))
	read_input(str(sys.argv[1]))
	# MS_Apriori(list_of_transactions, list_of_mis, SDC)
	#print(list_of_items)
	print(list_of_transactions)
	#print(list_of_mis)
else:
	print("Please run as python ms-apriori.py [input_file].txt [parameter_file].txt")
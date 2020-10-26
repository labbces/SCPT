#!/usr/bin/env python

import sys
import os
from ete3 import NCBITaxa
from collections import Iterable
from collections import defaultdict
from Bio import SeqIO

################################################################### 
# Ler kaiju file e criar dicionario com sequence ID e taxonomy ID #
###################################################################

def flatten(items):
	"""Yield items from any nested iterable.
	before: nested iterable = [['a'], ['b']]
	after: ['a', 'b']
	"""
	for x in items:
		if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
			for sub_x in flatten(x):
				yield sub_x
		else:
			yield x

ncbi = NCBITaxa()
descendants = ncbi.get_descendant_taxa("viridiplantae")

kaiju = "./20_SRR8771430.trimmed.kaiju"
def create_id_lists(kaiju, direction):
	""" Reading Kaiju file and creating the following lists by each ID:
	- taxonomy_id (3rd column)
	- taxonomy (integer)
	- sequence_id lists (2nd column)
	Direction must be "1/" or "/2"
	"""
	#Creating empty lists
	taxonomy_id = []
	sequence_id = []
	with open(kaiju, "r") as kaiju_file:
		for line in kaiju_file: 
			#Getting taxonomy and sequence ID from Kaiju file
			taxonomy_id.append(line.split()[2:3])
			sequence_id.append(line.split()[1:2]) 
			#Turn list of lists into flatten list - e.g: [['a'], ['b]] into ['a', 'b']
			sequence = list(flatten(sequence_id))
			taxonomy = list(flatten(taxonomy_id))
			#Add /1 and /2 to sequence ID
			sequence = [item + direction for item in sequence] 
                	#Turn str(items) into int(items)
			#That step is necessary to apply the descendants filter
			taxonomy = [int(i) for i in taxonomy]
		return taxonomy, sequence

###########################################
# CHECKING RESULTS OF 'create_id_lists()' #
###########################################

#Printing lists from Kaiju file
taxonomy_list, sequence_list = create_id_lists(kaiju, "/1")
#print("taxonomy list =", taxonomy_list)
#print("sequence list =", sequence_list)

#################################
# CREATING RAW KAIJU DICTIONARY #
#################################

def raw_kaiju_dict(taxonomy, sequence):
	""" Getting taxonomy, sequence lists and create raw Kaiju dictionary.
	kaiju_dictionary = (taxonomy, sequence) 
	"""
	kaiju_dict = defaultdict(list)
	for k, v in zip(taxonomy, sequence):
		kaiju_dict[k].append(v)
	return kaiju_dict

##########################################
# CHECKING RESULTS OF 'raw_kaiju_dict()' #
##########################################

kaiju_dict = raw_kaiju_dict(taxonomy_list, sequence_list)
#print("raw kaiju dict =", kaiju_dict)

######################################
# CREATING FILTERED KAIJU DICTIONARY #
######################################

def filter_for_kaiju_dict(kaiju_dict):
	""" Apply a filter to raw Kaiju dictionary.
	This filter is based in the taxonomy level inserted by the user.
	e.g of filter = "viridiplantae"
	"""
	filtered_kaiju_dict = {}
	for (key, value) in kaiju_dict.items():
		if key in descendants:
			filtered_kaiju_dict[key] = value	
	return filtered_kaiju_dict

#################################################
# CHECKING RESULTS OF 'filter_for_kaiju_dict()' #
#################################################

filtered_kaiju_dict = filter_for_kaiju_dict(kaiju_dict)
#print("filtered_kaiju_dict", filtered_kaiju_dict)

##############################################
# APPLY TAXONOMY LEVEL FILTER TO FASTQ FILES #
##############################################

filtered_R1 = []
filtered_R2 = []

for i in filtered_kaiju_dict.values():
	ids = list(flatten(filtered_kaiju_dict.values()))
	#print("filtered key values", ids)

fastq_parser = SeqIO.parse("./20_SRR8771430.trimmed.R1.fastq", "fastq")
for fastq_rec in fastq_parser:
	#print(fastq_rec.id)
	if fastq_rec.id in ids:
		filtered_R1.append(fastq_rec.format("fastq"))
		#print("filtered R1", filtered_R1)
		#print("sequence in dict", fastq_rec.format("fastq"))

new_R1 = open("./filtered_R1.fastq", "a+")
for i in filtered_R1:
	new_R1.writelines(i)
new_R1.close()



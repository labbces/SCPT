#!/usr/bin/env python

'''						Description
			This script removes contaminated sequences from FASTQ files!
		The user determines the sequences that must be maintained from a Taxonomy Level.
	if Taxonomy Level = "Viridiplantae": Only descendants from "Viridiplantae" will be maintained.
'''

import argparse
import sys
import os
from ete3 import NCBITaxa
from collections import Iterable
from collections import defaultdict
from Bio import SeqIO

# Creating arguments

parser = argparse.ArgumentParser(description='Removes contaminated sequences from Taxonomy Level in FASTQ files', add_help=True)
parser.add_argument('-k', '--kaiju_file', dest='kaiju_file', metavar='file', help='A .kaiju file with kaiju reports', required=True)
parser.add_argument('-R1', dest='R1_file', metavar='file', help='R1 FASTQ file', required=True)
parser.add_argument('-R2', dest='R2_file', metavar='file', help='R2 FASTQ file', required=True)
parser.add_argument('-t', '--taxonomy_level', dest='taxonomy_level', metavar='Tax rank', type=str, help='Only descendants from this Taxonomy Level will be maintained',required=True)

# Getting arguments

args = parser.parse_args()
kaiju_file = args.kaiju_file
R1 = args.R1_file
R2 = args.R2_file
taxonomy_level = args.taxonomy_level

# Getting taxonomy database and taxonomy level

ncbi = NCBITaxa()
descendants = ncbi.get_descendant_taxa(taxonomy_level)

# Turn nested iterable into list 

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

# Create taxonomy and sequences list

def create_id_lists(kaiju_file, direction):
	""" Reading Kaiju file and creating the following lists by each ID:
	- taxonomy_id (3rd column)
	- taxonomy (integer)
	- sequence_id lists (2nd column)
	"""
	#Checking fastq files direction
	##if "R1" in R1:
	        ##direction = "/1"
        	#print(direction)
	##elif "R2" in R2:
        	##direction = "/2"
        	#print(direction)
	##else:
        	##print("File {} isn't a R1 or R2 file".format(R1))
        	##exit()

	#Creating empty lists
	taxonomy_id = []
	sequence_id = []
	with open(kaiju_file, "r") as kaiju_file:
		for line in kaiju_file:
			if not line.startswith("U"): 
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
		print("Listas prontas!")
		return taxonomy, sequence

# CHECKING RESULTS OF 'create_id_lists()'

##taxonomy_list, sequence_list = create_id_lists(kaiju_file, direction)
#print("taxonomy list =", taxonomy_list)
#print("sequence list =", sequence_list)

# Creating raw kaiju dictionary 

def raw_kaiju_dict(taxonomy, sequence):
	""" Getting taxonomy, sequence lists and create raw Kaiju dictionary.
	kaiju_dictionary = (taxonomy, sequence) 
	"""
	kaiju_dict = defaultdict(list)
	for k, v in zip(taxonomy, sequence):
		kaiju_dict[k].append(v)
	print("raw dictionary pronto!")
	return kaiju_dict

# CHECKING RESULTS OF 'raw_kaiju_dict()'

##kaiju_dict = raw_kaiju_dict(taxonomy_list, sequence_list)
#print("raw kaiju dict =", kaiju_dict)

# Creating filtered kaiju dictionary

def filter_for_kaiju_dict(kaiju_dict):
	""" Apply a filter to raw Kaiju dictionary.
	This filter is based in the taxonomy level inserted by the user.
	e.g of filter = "viridiplantae"
	"""
	filtered_kaiju_dict = {}
	for (key, value) in kaiju_dict.items():
		if key in descendants:
			filtered_kaiju_dict[key] = value
	print("filtered kaiju dictionary pronto!")	
	return filtered_kaiju_dict

# CHECKING RESULTS OF 'filter_for_kaiju_dict()'

##filtered_kaiju_dict = filter_for_kaiju_dict(kaiju_dict)
#print("filtered_kaiju_dict", filtered_kaiju_dict)

# Apply Taxonomy Level filter to FASTQ files 

filtered_file_R1 = R1[:10] + ".trimmed.R1.filtered.fastq"
filtered_file_R2 = R2[:10] + ".trimmed.R2.filtered.fastq"
filtered_R1 = []
filtered_R2 = []
R_files = [R1, R2]

for i in R_files:
        if "R1" in i:
                direction = "/1"
		taxonomy_list, sequence_list = create_id_lists(kaiju_file, direction)
		kaiju_dict = raw_kaiju_dict(taxonomy_list, sequence_list)
		filtered_kaiju_dict = filter_for_kaiju_dict(kaiju_dict)
		for i in filtered_kaiju_dict.values():
			 ids = list(flatten(filtered_kaiju_dict.values()))
			#print("filtered key values", ids)
		fastq_parser = SeqIO.parse(R1, "fastq")
		for fastq_rec in fastq_parser:
        		#print(fastq_rec.id)
        		if fastq_rec.id in ids:
				filtered_R1.append(fastq_rec.format("fastq"))
				#print("filtered R1", filtered_R1)
				#print("sequence in dict", fastq_rec.format("fastq"))

		new_R1 = open(filtered_file_R1, "a+")
		for i in filtered_R1:
		      new_R1.writelines(i)
		new_R1.close()
		print("Filtered R1 was created as {}!".format(filtered_file_R1))

        elif "R2" in i:
                direction = "/2"
                taxonomy_list, sequence_list = create_id_lists(kaiju_file, direction)
		kaiju_dict = raw_kaiju_dict(taxonomy_list, sequence_list)
		filtered_kaiju_dict = filter_for_kaiju_dict(kaiju_dict)
                for i in filtered_kaiju_dict.values():
                         ids = list(flatten(filtered_kaiju_dict.values()))
                        #print("filtered key values", ids)
                fastq_parser = SeqIO.parse(R2, "fastq")
                for fastq_rec in fastq_parser:
                        #print(fastq_rec.id)
                        if fastq_rec.id in ids:
                                filtered_R2.append(fastq_rec.format("fastq"))
                                #print("filtered R2", filtered_R1)
                                #print("sequence in dict", fastq_rec.format("fastq"))

                new_R2 = open(filtered_file_R2, "a+")
                for i in filtered_R2:
                      new_R2.writelines(i)
                new_R2.close()
		print("Filtered R2 was created as {}!".format(filtered_file_R2))


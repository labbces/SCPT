#!/usr/bin/env python

import sys
from ete3 import NCBITaxa

################################################################### 
# Ler kaiju file e criar dicionario com sequence ID e taxonomy ID #
###################################################################

#from typing import Iterable 
from collections import Iterable                            # < py38

def flatten(items):
    """Yield items from any nested iterable."""
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten(x):
                yield sub_x
        else:
            yield x

#Empty lists and filtered dict
taxonomy_id = []  
sequence_id = [] 
kaiju_dict = {} 
key = 1
ncbi = NCBITaxa()
descendants = ncbi.get_descendant_taxa("viridiplantae")

#reading kaiju file and creating taxonomy_id, taxonomy (integer), sequence_id lists
#with open("./2_seq.kaiju", "r") as kaiju_file:
with open("20_SRR8771430.trimmed.kaiju", "r") as kaiju_file:
	for line in kaiju_file: 
		#getting taxonomy and sequence ID from kaiju file
		taxonomy_id.append(line.split()[2:3]) 
		sequence_id.append(line.split()[1:2]) 
		#turn list of lists in flatten list - [['a'], ['b]] into ['a', 'b']
		sequence = list(flatten(sequence_id))
		taxonomy = list(flatten(taxonomy_id)) 
                #turn str into int
		taxonomy = [int(i) for i in taxonomy]   ## need this step to apply the descendants filter
                #sequence = [int(i) for i in sequence]  ## dont need this
		#using zip dict constructor to create a dict with 2 lists
		##zip_dict = zip(taxonomy, sequence)
		##kaiju_dict = dict(zip_dict)	

from collections import defaultdict

my_dict = defaultdict(list)
for k, v in zip(taxonomy, sequence):
	my_dict[k].append(v)

print("my dict =", my_dict)

#print("zip_dict =", zip_dict)
print("raw taxonomy id list =", taxonomy_id) 
print("flatten taxonomy list =", taxonomy)
print("flatten taxonomy length =", len(taxonomy)) 
print("raw sequence list =", sequence_id)
print("flatten sequence list =", sequence) 
print("raw sequence length =", len(sequence))
#print("flatten kaiju_dict = ", kaiju_dict) 

######################################################################################
# creating filtered_dict based in presence of the taxid in the descendants user rank #		
######################################################################################

filtered_kaiju_dict = {}
##for (key, value) in kaiju_dict.items():
for (key, value) in my_dict.items():
	##print(key)
	if key in descendants:
		filtered_kaiju_dict[key] = value	

print("filtered_kaiju_dict", filtered_kaiju_dict)

##################################################################################
# read fastq files and write new file if sequence are in the filtered_kaiju_dict #
##################################################################################
from Bio import SeqIO
import os

#R1 = open("./2_seq_R1.fastq")
R2 = open("./2_seq_R2.fastq")
filtered_R1 = []
filtered_R2 = []

for i in filtered_kaiju_dict.values():
	ids = list(flatten(filtered_kaiju_dict.values()))
	print("filtered key values", ids)

fastq_parser = SeqIO.parse("./20_SRR8771430.trimmed.R1.fastq", "fastq")
for fastq_rec in fastq_parser:
	print(fastq_rec.id)
	#if fastq_rec.id in filtered_kaiju_dict.values():
	if fastq_rec.id in ids:
		filtered_R1.append(fastq_rec.format("fastq"))
		print("filtered R1", filtered_R1)
		#print("sequence in dict", fastq_rec.format("fastq"))

new_R1 = open("./filtered_R1.fastq", "a+")
for i in filtered_R1:
	new_R1.writelines(i)
new_R1.close()

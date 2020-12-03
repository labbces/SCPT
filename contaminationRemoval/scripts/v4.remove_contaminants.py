#!/usr/bin/env python

'''						Description
			This script removes contaminated sequences from FASTQ files!
		The user determines the sequences that must be maintained from a Taxonomy Level.
	if Taxonomy Level = "Viridiplantae": Only descendants from "Viridiplantae" will be maintained.
				Requirements: R1.fastq and R2.fastq index_db
'''

import argparse
import sys
import os
from ete3 import NCBITaxa
from collections import Iterable
from collections import defaultdict
from Bio import SeqIO

# Creating arguments

parser = argparse.ArgumentParser(prog='remove_contaminants.py', description='Removes contaminated sequences from Taxonomy Level in FASTQ files', add_help=True)
parser.add_argument('-k', dest='kaiju_file', metavar='<.kaiju file>', help='A .kaiju file with kaiju reports', required=True)
parser.add_argument('-R1', dest='R1_file', metavar='<R1 file>', help='R1 FASTQ file', required=True)
parser.add_argument('-R2', dest='R2_file', metavar='<R1 file>', help='R2 FASTQ file', required=True)
parser.add_argument('-t', dest='taxonomy_level', metavar='<Taxonomy level>', type=str, help='Only descendants from this Taxonomy Level will be maintained',required=True)
parser.add_argument('-v', '--version', action='version', version='%(prog)s v4.2')

# Getting arguments

args = parser.parse_args()
kaiju_file = args.kaiju_file
R1 = args.R1_file
R2 = args.R2_file
taxonomy_level = args.taxonomy_level

# Opening fastq files index_db

try:
	index_R1 = SeqIO.index_db(R1[:-5] + "index")
except ValueError:
	print("{} Dont exist. Please create an index_db for the R1_fastq_files running 'create_index_db.py'".format(R1[:-5] + "index"))

try:
	index_R2 = SeqIO.index_db(R2[:-5] + "index")
except ValueError:
        print("{} Dont exist. Please create an index_db for the R2_fastq_files running 'create_index_db.py'".format(R2[:-5] + "index"))
	sys.exit(1)	

# Getting taxonomy database and taxonomy level

ncbi = NCBITaxa()
descendants = ncbi.get_descendant_taxa(taxonomy_level, intermediate_nodes=True) # Getting intermediate nodes, like Streptophyta (35493) 

# Getting user taxonomy level and append to descendants 

name2taxid = ncbi.get_name_translator([taxonomy_level])
user_tax_id = name2taxid.values()[0][0] # Getting first item in list of list, e.g [[item]].
descendants.append(user_tax_id)

'''	Just to confirm if user_taxid_id is within descendants
if user_tax_id in descendants:
	print("user_taxid in descendants = True")
else:
	print("user_taxid in descendants = False")
'''


# Create filtered files names

filtered_R1 = kaiju_file[19:22] + R1[:-8] + "filtered.R1.fastq"
filtered_R2 = kaiju_file[19:22] + R2[:-8] + "filtered.R2.fastq"
unfiltered_R1 = kaiju_file[19:22] + R1[:-8] + "unclassified.R1.fastq"
unfiltered_R2 = kaiju_file[19:22] + R2[:-8] + "unclassified.R2.fastq"

#Create counter

count_filtered_sequences = 0
count_unclassified_sequences = 0

# Filtering and creating files

with open(kaiju_file, "r") as kaiju, open(filtered_R1, "w") as classified_R1, open(filtered_R2, "w") as classified_R2, open(unfiltered_R1, "w") as unclassified_R1, open(unfiltered_R2, "w") as unclassified_R2:
	for line in kaiju:

		# Getting IDs

		R1_sequence_id = line.split()[1] + "/1"
                R2_sequence_id = line.split()[1] + "/2"
		taxonomy_id = int(line.split()[2])

		# Getting sequences in descendants (user taxonomic level)

		if line.startswith("C") and taxonomy_id in descendants:
			count_filtered_sequences += 1
			SeqIO.write(index_R1[R1_sequence_id], classified_R1, "fastq")
                       	SeqIO.write(index_R2[R2_sequence_id], classified_R2, "fastq")

		# Getting unclassified reads in kaiju file

		elif line.startswith("U"):
			count_unclassified_sequences += 1
			SeqIO.write(index_R1[R1_sequence_id], unclassified_R1, "fastq")
			SeqIO.write(index_R2[R2_sequence_id], unclassified_R2, "fastq")
	
	print("{} sequences classified by Kaiju are within the taxonomic level {}.".format(count_filtered_sequences, taxonomy_level))
	print("{} sequences are unclassified by Kaiju".format(count_unclassified_sequences))
	print("Filtered files was created as {} and {}".format(filtered_R1, filtered_R2))
       	print("Unclassified files was created as {} and {}".format(unfiltered_R1, unfiltered_R2))

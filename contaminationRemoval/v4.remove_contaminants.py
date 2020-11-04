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

parser = argparse.ArgumentParser(prog='remove_contaminants.py', description='Removes contaminated sequences from Taxonomy Level in FASTQ files', add_help=True)
parser.add_argument('-k', dest='kaiju_file', metavar='<.kaiju file>', help='A .kaiju file with kaiju reports', required=True)
parser.add_argument('-R1', dest='R1_file', metavar='<R1 file>', help='R1 FASTQ file', required=True)
parser.add_argument('-R2', dest='R2_file', metavar='<R1 file>', help='R2 FASTQ file', required=True)
parser.add_argument('-t', dest='taxonomy_level', metavar='<Taxonomy level>', type=str, help='Only descendants from this Taxonomy Level will be maintained',required=True)
parser.add_argument('-v', '--version', action='version', version='%(prog)s v4.0')

# Getting arguments

args = parser.parse_args()
kaiju_file = args.kaiju_file
R1 = args.R1_file
R2 = args.R2_file
taxonomy_level = args.taxonomy_level

# Open indexdb

try:
	index_R1 = open(R1[:-5] + "index", "r")
except IOError:
	print(R1[:-5] + "index", "dont exist. Please create the indexdb for fastq files running 'create_index_db.py'")

try:
        index_R2 = open(R2[:-5] + "index", "r")
except IOError:
        print(R2[:-5] + "index", "dont exist. Please create the indexdb for fastq files running 'create_index_db.py'")

#index_db_R1 = R1[:-5] + "index"
#index_db_R2 = R2[:-5] + "index"

# Getting taxonomy database and taxonomy level

ncbi = NCBITaxa()
descendants = ncbi.get_descendant_taxa(taxonomy_level)

# Create filtered files names

filtered_R1 = R1[:-8] + "filtered.R1.fastq"
filtered_R2 = R2[:-8] + "filtered.R2.fastq"
unfiltered_R1 = R1[:-8] + "unclassified.R1.fastq"
unfiltered_R2 = R2[:-8] + "unclassified.R2.fastq"

# Read fastq index

record_R1_dict = SeqIO.index_db(index_db_R1, "fastq")
record_R2_dict = SeqIO.index_db(index_db_R2, "fastq")


with open(kaiju_file, "r") as kaiju, open(filtered_R1, "w") as classified_R1, open(filtered_R2, "w") as classified_R2, open(unfiltered_R1, "w") as unclassified_R1, open(unfiltered_R2, "w") as unclassified_R2:
	for line in kaiju:

		# Getting IDs

		R1_sequence_id = line.split()[1] + "/1"
                R2_sequence_id = line.split()[1] + "/2"
		taxonomy_id = int(line.split()[2])

		# To avoid long time processing - looking only at classified reads

		if line.startswith("C") and taxonomy_id in descendants and R1_sequence_id in index_R2.keys():
			SeqIO.write(record_R1_dict[R1_sequence_id], classified_R1, "fastq")
                       	SeqIO.write(record_R2_dict[R2_sequence_id], classified_R2, "fastq")

		# If line.startswith("U") or line.startswith("C") and isnt in descendants

		else:
			if R1_sequence_id in index_R2.keys():
				SeqIO.write(record_R1_dict[R1_sequence_id], unclassified_R1, "fastq")
				SeqIO.write(record_R2_dict[R2_sequence_id], unclassified_R2, "fastq")
	print("Filtered files was created as {} and {}".format(filtered_R1, filtered_R2))
       	print("Unclassified files was created as {} and {}".format(unfiltered_R1, unfiltered_R2))

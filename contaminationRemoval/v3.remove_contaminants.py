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

# Create filtered files names

filtered_R1 = R1[:10] + ".trimmed.R1.filtered.fastq"
filtered_R2 = R2[:10] + ".trimmed.R2.filtered.fastq"
unfiltered_R1 = R1[:10] + ".trimmed.R1.unclassified.fastq"
unfiltered_R2 = R2[:10] + ".trimmed.R2.unclassified.fastq"

# Create index for fastq files

# For large files isnt possible to hold everything in memory, so to_dict is not suitable
#record_R1_dict = SeqIO.to_dict(SeqIO.parse(R1, "fastq"))
#record_R2_dict = SeqIO.to_dict(SeqIO.parse(R2, "fastq"))

# For large files, I can use .index function
record_R1_dict = SeqIO.index(R1, "fastq")
print("Index for {} was created".format(R1))
record_R2_dict = SeqIO.index(R2, "fastq")
print("Index for {} was created".format(R2))

with open(kaiju_file, "r") as kaiju, open(filtered_R1, "w") as classified_R1, open(filtered_R2, "w") as classified_R2, open(unfiltered_R1, "w") as unclassified_R1, open(unfiltered_R2, "w") as unclassified_R2:
	for line in kaiju:
		# To avoid long time processing - looking only at classified reads
		if line.startswith("C"):
			if int(line.split()[2]) in descendants:
				R1_sequence_id = line.split()[1] + "/1"
				R2_sequence_id = line.split()[1] + "/2"
				taxonomy_id = line.split()[2]
				if R1_sequence_id in record_R1_dict.keys():
					SeqIO.write(record_R1_dict[R1_sequence_id], classified_R1, "fastq")
                                       	SeqIO.write(record_R2_dict[R2_sequence_id], classified_R2, "fastq")
		else:
			unclassified_R1_sequence_id = line.split()[1] + "/1"
			unclassified_R2_sequence_id = line.split()[1] + "/2"
			unclassified_taxonomy_id = line.split()[2]
			SeqIO.write(record_R1_dict[unclassified_R1_sequence_id], unclassified_R1, "fastq")
			SeqIO.write(record_R2_dict[unclassified_R2_sequence_id], unclassified_R2, "fastq")
	print("Filtered files was created as {} and {}".format(filtered_R1, filtered_R2))
        print("Unclassified files was created as {} and {}".format(unfiltered_R1, unfiltered_R2))



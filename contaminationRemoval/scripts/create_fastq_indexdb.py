#!/usr/bin/env python

'''				Description
		This script creates a indexdb for FASTQ files!
		This step is necessary to run remove_contaminants.py
'''

import argparse
import sys
import os
from Bio import SeqIO

# Creating arguments

parser = argparse.ArgumentParser(prog='create_indexdb.py', description='create indexdb for FASTQ files', add_help=True)
parser.add_argument('-R1', dest='R1_file', metavar='<R1 file>', help='R1 FASTQ file')
parser.add_argument('-R2', dest='R2_file', metavar='<R1 file>', help='R2 FASTQ file')
parser.add_argument('-v', '--version', action='version', version='%(prog)s v1.0')

#fixing
parser.add_argument('-R0', dest='R0_file', metavar='<R0 file>', help='R0 FASTQ file')

# Getting arguments

args = parser.parse_args()
R0 = args.R0_file
R1 = args.R1_file
R2 = args.R2_file

# Generate index names 

# Check-in

single = 0
paired = 0
final_format = "test"

if ".fasta" in R0 or R2:
	final_format = "fasta"
	print("Input detected in fasta format")
	
if ".fastq" in R0 or R2:
	final_format = "fastq"
	print("Input detected in fastq format")

if R2 in args:
	paired = 1
	single = 0
	print("Creating indexdb for paired-end reads")
else: 
	paired = 0
	single = 1
	print("Creating indexdb for single-end reads!")

if single == 1:
#Name: AllSyntheticLongReads.fasta.gz
	index_R0 = R0[:-5] + "index"

	# Create indexdb for large fastq files - This process dramatically decreases the runtime and RAM usage when compared to dictionaries.

	record_R0_index_db = SeqIO.index_db(index_R0, R0, final_format)
	print("Indexdb created!")
else: 
	index_R1 = R1[:-5] + "index"
	index_R2 = R2[:-5] + "index"

	# Create indexdb for large fastq files - This process dramatically decreases the runtime and RAM usage when compared to dictionaries.

	record_R1_index_db = SeqIO.index_db(index_R1, R1, final_format)
	record_R2_index_db = SeqIO.index_db(index_R2, R2, final_format)
	print("Indexdb created!")

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
parser.add_argument('-R1', dest='R1_file', metavar='<R1 file>', help='R1 FASTQ file', required=True)
parser.add_argument('-R2', dest='R2_file', metavar='<R1 file>', help='R2 FASTQ file', required=True)
parser.add_argument('-v', '--version', action='version', version='%(prog)s v1.0')

# Getting arguments

args = parser.parse_args()
R1 = args.R1_file
R2 = args.R2_file

# Generate index names 

index_R1 = R1[:-5] + "index"
index_R2 = R2[:-5] + "index"

# Create indexdb for large fastq files - This process dramatically decreases the runtime and RAM usage when compared to dictionaries.

record_R1_index_db = SeqIO.index_db(index_R1, R1, "fastq")
record_R2_index_db = SeqIO.index_db(index_R2, R2, "fastq")

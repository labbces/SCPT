#!/usr/bin/env python

'''			Description
	This script counts the number of reads within
	user taxonomy id, unclassified reads and reads
	out the user taxonomy id.
'''

import argparse
import re
from ete3 import NCBITaxa

# Creating arguments

parser = argparse.ArgumentParser(prog='count_taxid.py', description='count taxid in kraken filtered files', add_help=True)
parser.add_argument('-k', dest='kraken_file', metavar='<.kraken file>', help='A .kraken file with kaiju reports', required=True)
parser.add_argument('-t', dest='taxonomy_level', metavar='<Taxonomy level>', type=str, help='Only descendants from this Taxonomy Level will be counted',required=True)
parser.add_argument('-v', '--version', action='version', version='%(prog)s v4.2')

# Getting arguments

args = parser.parse_args()
taxonomy_level = args.taxonomy_level
kraken_file = args.kraken_file

# Getting NCBITaxa

ncbi = NCBITaxa()
descendants = ncbi.get_descendant_taxa(taxonomy_level)

# Creating counter

viridiplantae_counter = 0
unclassified_counter = 0
contaminant_counter = 0

with open(kraken_file, "r") as kraken:
	for line in kraken.readlines():
		# Regex to get taxonomy names
		#taxonomy_name = re.sub(r" ?\([^)]+\)", "",('\t')[2])
		# Regex to get taxonomy id
		taxonomy_id = re.findall("\d+", line.split('\t')[2])
		# Turn str into int
		taxonomy_id = [int(x) for x in taxonomy_id]
		for i in taxonomy_id:
			if i in descendants:
				viridiplantae_counter += 1
			else:
				contaminant_counter += 1
			if line.startswith("U"):
				unclassified_counter += 1

print("Total Viridiplantae reads = {}".format(viridiplantae_counter))
print("Total contaminants reads = {}".format(contaminant_counter))
print("Total unclassified reads = {}".format(unclassified_counter))

#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(prog="generateSpeciesSequences.py", description="Generates SpeciesSequences.txt necessary to run OrthoFinder2 (keeping results from old blast search)", add_help=True)
parser.add_argument("-ids", dest="fasta_identifiers", metavar="<file with protein identifiers>", help="A fasta file containing genotype-specific proteins identifiers", required=True)
parser.add_argument("-n", dest="genotype_number", metavar="<genotype number>", help="genotype number", required=True)
parser.add_argument("-o", dest="output", metavar="<output name>", help="output name", required=True)

args = parser.parse_args()
fasta_identifiers = args.fasta_identifiers
genotype_number = args.genotype_number
out = fasta_identifiers + "Sequences.txt" 

with open(fasta_identifiers, "r+") as f:
  lines = f.readlines()
  f.seek(0)
  with open(out, "a+") as o:
    for index,line in enumerate(lines):
        #print("{}_{}: {}".format(genotype_number, index, line))
        o.write("{}_{}: {}".format(int(genotype_number), int(index), str(line)))
o.close()
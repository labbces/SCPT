#!/usr/bin/env python

# Generate SpeciesSequences.txt before run OrthoFinder2
# ids file must contains only the IDENTIFIER of the sequence, without ">", like this:
#
# B1_k25_TRINITY_DN10207_c0_g1_i2
# B1_k25_TRINITY_DN11245_c0_g3_i3
# B1_k25_TRINITY_DN11588_c0_g1_i7
# B1_k25_TRINITY_DN11940_c0_g1_i7
#
# generating ids file with sed:
# grep ">" fasta | sed 's/>//g' > fasta_identifiers

import argparse

parser = argparse.ArgumentParser(prog="generateSpeciesSequences.py", description="Generates SpeciesSequences.txt necessary to run OrthoFinder2 (keeping results from old blast search)", add_help=True)
parser.add_argument("-ids", dest="fasta_identifiers", metavar="<file with protein identifiers>", help="A fasta file containing genotype-specific proteins identifiers", required=True)
parser.add_argument("-n", dest="genotype_number", metavar="<genotype number>", help="genotype number", required=True)

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
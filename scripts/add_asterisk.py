#!/usr/bin/env python

import argparse
from Bio import SeqIO

parser = argparse.ArgumentParser(prog='Add asterisk')
parser.add_argument('-cds', dest='cds_file', required=True)

args = parser.parse_args()
cds_file = args.cds_file

output_name = cds_file[:-3] + "asterisk.fna"

with open(output_name, "w") as output_handle:
    for record in SeqIO.parse(cds_file, "fasta"):
        record.seq = record.seq + "*"
        SeqIO.write(record, output_handle, "fasta")

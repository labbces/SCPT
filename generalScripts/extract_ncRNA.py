#!/usr/bin/env python

import argparse
from Bio import SeqIO

#Extract putative ncRNA sequences from a transcriptome file based on their CDS sequences.

# Creating arguments
#parser = argparse.ArgumentParser(prog='Extract_ncRNAs.py', add_help=True)
parser = argparse.ArgumentParser(prog='Extract_ncRNA.py', description='a', add_help=True)
parser.add_argument('-transcriptome', '-t', dest='transcriptome_file', metavar='<transcriptome file>', required=True)
parser.add_argument('-protein', '-p', dest='protein_file', metavar='<protein file>', required=True)
parser.add_argument('-output', '-o', dest='ncRNA_file', metavar='<ncRNA file>', required=True)

#Getting arguments
args = parser.parse_args()
transcriptome_file = args.transcriptome_file
protein_file = args.protein_file
ncRNA_file = args.ncRNA_file

#Loading transcriptomes seq ID and proteins features
transcripts = list(SeqIO.parse(transcriptome_file, "fasta"))
dict_proteins = SeqIO.to_dict(SeqIO.parse(protein_file, "fasta"))

#Generate list with ncRNA sequences id
ncRNA_list = []
transcriptome_index = transcriptome_file[:-5] + "index"

for i in range(0, len(transcripts)):
    if transcripts[i].id not in dict_proteins.keys():
        ncRNA_list.append(transcripts[i].id)

#Generate index database for transcriptome (store sequence features)
transcriptome_db = SeqIO.index_db(transcriptome_index, transcriptome_file, "fasta")

#Generate ncRNA file
with open(ncRNA_file, "w") as ncRNA_output:
    for i in ncRNA_list:
        if i in transcriptome_db:
            SeqIO.write(transcriptome_db[i], ncRNA_output, "fasta")

#!/usr/bin/env python

###################################################################
# Extract contaminants from Kaiju and calculates their reads number
###################################################################

import argparse
import pandas as pd
import glob
import os

################################
# Command line arguments
################################

parser = argparse.ArgumentParser(description='Extract contaminants reads number from Kaiju reports (tsv file) ', add_help=True)
parser.add_argument('-i', '--input', dest='input', metavar='file', help='A .tsv file with Kaiju reports', required=True)
parser.add_argument('-p', '--percentage', dest='percentage', metavar='int', type=int, help='Contaminant percentage threshold', required=True)
parser.add_argument('-o', '--output', dest='output', metavar='file', help='Base name for extracted contaminants file',required=True)

################################
# Getting arguments
################################

args = parser.parse_args()
tsvFile = args.input
percentage = args.percentage
output = args.output + ".csv"

################################
# Extract threshold contaminants
################################

#This function creates a new file if the contamination ratio is > than percentage
def extract_contaminants(kaiju_tsv,percentage):
    print("Extracting contaminants with percentage threshold higher than",percentage,"...")
    table = pd.read_csv(tsvFile, sep="\t", skiprows=[0])
    # Adjusting the table index 
    table.columns = ['%', 'reads', 'species']
    # Converting column '%' into INT or NUMERIC only
    table['%'] = pd.to_numeric(table['%'], errors='coerce')
    # Creating filters for undesirable index
    table_remove = table.loc[(table["species"] == "unclassified") | 
    (table["species"] == "Viruses") |
    (table["species"] == "cannot be assigned to a species ")]
    # Removing the filters 
    filtered_df = table.drop(table_remove.index)
    # Apply the threshold condition
    extracted_df = filtered_df.loc[table["%"] > percentage]
    # Creating a new file with extracted lines (applied conditions)
    print("Creating file with extracted contaminants...")
    print("Extracted contaminants file was created as", output)
    return(extracted_df.to_csv(output, index = False))

extract_contaminants(tsvFile, percentage)

###
#TO DO: 
# pegar as duas ultimas palavras da coluna species e criar um dicionario vazio; 
# somar a quantidade de reads com linhas que possuem a mesma especie
# printar quantidade total de reads pra cada contaminant

#os.system("cat extracted_contaminants.csv | awk '{ s+=$2 } END { print s }'")
# The total_reads needs to be added manually, the number is the output from the sum of de second column
# of the extracted_contaminants.csv file
total_reads = 2454519
reads_lenght = 151
genome_size = 3940614
contaminant = "Acinetobacter baumannii"

# This function calculates the coverage of contaminants
# total reads = total sum of contaminants reads // reads_lenght = 151 // genome_size = contaminant genome size
def coverage_contaminants(total_reads, reads_lenght, genome_size):
    return((total_reads*2*reads_lenght)/genome_size)

##print("The", contaminant, "coverage is: ",coverage_contaminants(total_reads, reads_lenght, genome_size))
###

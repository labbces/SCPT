#!/usr/bin/env python

###################################################################
# Extract contaminants from Kaiju and calculates their reads number
###################################################################

'''
This script creates a new file if the contamination ratio is > than percentage
and prints the amount of reads for each contaminant
'''

import argparse
import pandas as pd
from pandas import DataFrame as df
import glob
import os

##########################################
# Creating arguments
##########################################

parser = argparse.ArgumentParser(description='Extract contaminants reads number from Kaiju reports (tsv file) ', add_help=True)
parser.add_argument('-i', '--input', dest='input', metavar='file', help='A .tsv file with Kaiju reports', required=True)
parser.add_argument('-p', '--percentage', dest='percentage', metavar='int', type=int, help='Contaminant percentage threshold', required=True)
parser.add_argument('-o', '--output', dest='output', metavar='file', help='Base name for extracted contaminants file',required=True)

##########################################
# Getting arguments
##########################################

args = parser.parse_args()
tsvFile = args.input
percentage = args.percentage
output = args.output + ".csv"

##########################################
# Extract and count threshold contaminants
##########################################

def extract_contaminants(kaiju_tsv,percentage):
    print("Extracting contaminants with percentage threshold higher than",percentage,"...")
    table = pd.read_csv(tsvFile, sep="\t", skiprows=[0])
    # Adjusting the table index 
    table.columns = ['%', 'reads', 'species']
    # Converting columns into INT or NUMERIC only
    table['%'] = pd.to_numeric(table['%'], errors='coerce')
    table['reads'] = pd.to_numeric(table['reads'], errors='coerce')
    # Creating filters for undesirable index
    table_remove = table.loc[(table["species"] == "unclassified") | 
    (table["species"] == "Viruses") |
    (table["species"] == "cannot be assigned to a species ")]
    # Removing the filters 
    filtered_df = table.drop(table_remove.index)
    # Apply the threshold condition
    extracted_df = filtered_df.loc[table["%"] > percentage]
    # Creating the output file with extracted lines (applied conditions)
    print("Creating file with extracted contaminants...")
    print("Extracted contaminants file was created as", output)
    newfile = extracted_df.to_csv(output, index = False)

    # SUPER INTERESTING, THIS IS SUUUUUPER INTERESTING:
    # A groupby operation involves some combination of splitting the object,
    # applying a function, and combining the results. This can be used to group 
    # large amounts of data and compute operations on these groups.

    # Creating a dictionary and calculate the amount of reads per contaminant in one line :O
    counting = extracted_df["reads"].groupby(extracted_df["species"]).apply(sum).to_dict()
    return(print(counting))

extract_contaminants(tsvFile, percentage)

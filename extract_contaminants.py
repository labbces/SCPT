#!/usr/bin/env python

####################################################################
### EXTRACT CONTAMINANTS FROM KAIJU AND CALCULATE THEIR COVERAGE ###
####################################################################

# TO DO:
# create a argparser for this script

import pandas as pd
import glob
import os

###
# This function concatenates all the kaiju reports into one csv file
# all_type must be like 'endswith': "*.trimmed.kaiju_speciesSummary.tsv"
#UPDATE: After the summary from ALL of the kaiju.tsv output from the server, this function is useless
def concatenate(path_to_tsv, all_type):
    os.chdir(path_to_tsv)
    extension = all_type
    all_filenames = [i for i in glob.glob(extension)]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames], sort=True)
    combined_csv.to_csv("all_kaiju_reports.csv", index=False, encoding='utf-8-sig')
    return(print("As tabelas foram concatenadas no novo arquivo: all_kaiju_reports.csv"))

path_to_tsv = "/home/felipe/Documentos/Sugarcane/MyAssembly_Hoang_2017_Illumina/kaiju_reports/"
# Call to concatenate all *tsv in the path
##concatenate(path_to_tsv, "*.trimmed.kaiju_speciesSummary.tsv")
###

###
# This function creates a new file if the contamination ratio is > than percentage
# kaiju_tsv = concatenated files ("summary.tsv") // percentage = contamination ratio (int)
def extract_contaminants(kaiju_tsv,percentage):
    print("Extraindo contaminantes com porcentagem de reads acima de", percentage)
    table = pd.read_csv(kaiju_tsv, sep="\t", skiprows=[0])
    # Adjusting the table index 
    table.columns = ['%', 'reads', 'species']
    # Converting column '%' into INT or NUMERIC only
    table['%'] = pd.to_numeric(table['%'], errors='coerce')
    # Creating filters to remove undesirable index
    table_remove = table.loc[(table["species"] == "unclassified") | 
    (table["species"] == "Viruses") |
    (table["species"] == "cannot be assigned to a species ")]
    # Apply filters into a new DF
    filtered_df = table.drop(table_remove.index)
    # Apply the ratio condition
    extracted_df = filtered_df.loc[table["%"] > percentage]
    # Creating a new file with extracted lines (applied conditions)
    return(extracted_df.to_csv("extracted_contaminants.csv", index = False))

path_to_summary_tsv = "/home/felipe/Documentos/Sugarcane/MyAssembly_Hoang_2017_Illumina/kaiju_reports/summary.tsv"
##extract_contaminants(path_to_summary_tsv, 1)
###

###
os.system("cat extracted_contaminants.csv | awk '{ s+=$2 } END { print s }'")
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

print("The", contaminant, "coverage is: ",coverage_contaminants(total_reads, reads_lenght, genome_size))
###

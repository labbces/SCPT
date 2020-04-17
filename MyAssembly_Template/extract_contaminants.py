####################################################################
### EXTRACT CONTAMINANTS FROM KAIJU AND CALCULATE THEIR COVERAGE ###
####################################################################

### BRAINSTORM AREA
#  
# 1. read multiple files // or // concatenate all the kaiju files
# 2. create a dictionary with species taxons e.g ({specie: Acinetobacter baumanii})
# 3. if percentage > 1: store the reads number in the specie dctionary e.g ({Acinetobacter baumanii: 63093})
# 4. if {specie: Acinetobacter baumanii} exists and their percentage > 1: sum the reads in the dict (63093 + 51308)
# 5. print the total sum of each {specie} reads
#
### BRAINSTORM AREA

import pandas as pd
import glob
import os

# This function concatenates all the kaiju reports into one csv file
# files must be like 'endswith' string: "*.trimmed.kaiju_speciesSummary.tsv"
# THIS POINTS NEEDS TO BE FIXED:
# * Remove "-" in "%" columns;
# * Remove "cannot be assigned to a species" in "species" columns;
# * Remove "unclassified" in "species" columns
def concatenate(files):
    os.chdir("/home/felipe/Documentos/Sugarcane/MyAssembly_Hoang_2017_Illumina/kaiju_reports/")
    extension = files
    all_filenames = [i for i in glob.glob(extension)]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames], sort=True)
    combined_csv.to_csv("all_kaiju_reports.csv", index=False, encoding='utf-8-sig')
    return(print("As tabelas foram concatenadas no novo arquivo: all_kaiju_reports.csv"))


# This function extract contaminants information if the contamination ratio is > than percentage
# kaiju_tsv = concatenated files // percentage = contamination ratio (int)
# WORKING FINE :)
def extract_contaminants(kaiju_tsv,percentage):
    # Open the Kaiju table report without second line (skiprows[1]) = "(--------)"
    table = pd.read_csv(kaiju_tsv, sep="\t")#, nrows=5, skiprows=[1])
    # Adjusting the table index 
    adjust_table = table.columns = ['%', 'reads', 'species']
    # Returning lines with contamination ratio > than percentage (%) 
    return(table.loc[table["%"] > percentage])

# I need to find a better way to call path and filename inside extract_contaminants function
path = "/home/felipe/Documentos/Sugarcane/MyAssembly_Hoang_2017_Illumina/kaiju_reports/"
filename = "all_kaiju_reports.csv"
#print(extract_contaminants(path + filename, 1))

# This function calculates the coverage of contaminants
# total reads = total sum of contaminants reads // reads_lenght = 151 // genome_size = contaminant genome size
def coverage_contaminants(total_reads, reads_lenght, genome_size):
    return((total_reads)*2*(reads_lenght)/genome_size)

#print("contaminant coverage =", coverage_contaminants(20000,151,30000))
#!/usr/bin/env python

import pandas as pd
import numpy as np
from math import factorial
import sys
import argparse

# creating arguments
parser = argparse.ArgumentParser(prog = "extract_pan_transcriptome_data.py", description="Extract core- and pan-transcriptome size from OrthoFinder GeneCount output", add_help=True)
parser.add_argument("-i", dest="input_file", metavar="<Orthogroups.GeneCount.tsv>", help="OrthoFinder GeneCount output", required=True)

# getting arguments
args = parser.parse_args()
input_file = args.input_file
output_file = "Pan-Transcriptome_data_mod." + input_file
output_pan = "Pan-Transcriptome_Size." + input_file
output_core = "Core-Transcriptome_Size." + input_file
output_accessory = "Accessory-Transcriptome_Size." + input_file
output_exclusive = "Exclusive-Transcriptome_Size." + input_file

# setting recursion limit to 1000000
sys.setrecursionlimit(10**6)

# loading input data
data = pd.read_csv(input_file, delimiter='\t', header=0, index_col=0)

print(f'{data.shape}')

myColNames=data.columns

if 'Total' in myColNames:
    print(f'WARNING:You have a Total column, we are dropping it. If that is not what you want change the name')
    data.drop(columns=['Total'], inplace=True)

print(f'{data.shape}')


# loading output file

def sample_random_selection(data, samples):
    my_sample = data.sample(number_genotypes, axis='columns', replace=False)
    
    my_selection = sorted(list(my_sample.columns))
    #print(f"sample dentro da funcao: {samples}, my_selection: {my_selection}; my_sample columns: {sorted(list(my_sample.columns))}")
    if 'Total' in my_selection:
        sys.exit("You imput dataframe is including a total column, please fix this. We are dying here!")
    if my_selection in samples:
        sample_random_selection(data, samples)
    else:
        samples.append(my_selection)
    return(my_sample, samples)

with open(output_file, "a") as write_output_file:#, open(output_pan, "a") as write_output_pan, open(output_core, "a") as write_output_core, open(output_accessory, "a") as write_output_accessory, open(output_exclusive, "a") as write_output_exclusive:
    for number_genotypes in range(1, data.shape[1]):
        print(f'{number_genotypes} samples {data.shape[1]}')
        max_n_sample = 20
        #print(number_genotypes)
        samples = []

        max_number_of_samples = int(factorial(data.shape[1]-1) / factorial((data.shape[1]-1 - number_genotypes)))
        if max_number_of_samples < max_n_sample:
            max_n_sample = max_number_of_samples
        #print(max_n_sample)
        for n_sample in range(0, max_n_sample):
            pan_transcriptome_size = 0
            genes_pan = 0
            accessory_transcriptome_size = 0
            genes_accessory = 0
            core_transcriptome_size = 0
            genes_core = 0
            exclusive_transcriptome_size = 0
            genes_exclusive = 0
            
            #print(f"samples: {samples}; n_sample: {n_sample}" )
            my_sample,samples = sample_random_selection(data, samples)
            my_sample = np.array(my_sample)
            #print(f'number genotypes: {number_genotypes}; sample number: {n_sample}; genotypes: {list(my_sample.columns)}')
            #print(my_sample)

            for orthogroup in my_sample:
                # print(f'{orthogroup}')
                number_of_genotypes_in_orthogroups = 0  
                if sum(orthogroup) > 0:
                    #number_of_genotypes_in_orthogroups += 1
                    genes_pan += sum(orthogroup)
                    pan_transcriptome_size += 1
                    for genotype in orthogroup:
                        if genotype > 0:
                            number_of_genotypes_in_orthogroups += 1
                        
                #core > 90%
                #accessory = X < 0.9 and X > only 1 genotype 
                #exclusive = only 1 genotype
                
                    if number_of_genotypes_in_orthogroups / number_genotypes > 0.9:
                        genes_core += sum(orthogroup)
                        core_transcriptome_size += 1
                        
                    if number_of_genotypes_in_orthogroups / number_genotypes < 0.9 and number_of_genotypes_in_orthogroups > 1:
                        genes_accessory += sum(orthogroup)
                        accessory_transcriptome_size += 1
                                        
                    if number_of_genotypes_in_orthogroups == 1:
                        genes_exclusive += sum(orthogroup)
                        exclusive_transcriptome_size += 1

                #print(f"pan_transcriptome_size: {pan_transcriptome_size} \t core_transcriptome_size: {core_transcriptome_size} \t number_genotypes: {number_genotypes} \t n_sample: {n_sample}")

                write_output_file.write("pan_transcriptome_size:" + str(pan_transcriptome_size) + "\t"
                                    + "genes_pan:" + str(genes_pan) + "\t"
                                    + "core_transcriptome_size:" + str(core_transcriptome_size) + "\t"
                                    + "genes_core:" + str(genes_core) + "\t"
                                    + "accessory_transcriptome_size:" +str(accessory_transcriptome_size) + "\t"
                                    + "genes_accessory:" + str(genes_accessory) + "\t"
                                    + "exclusive_transcriptome_size:" + str(exclusive_transcriptome_size) + "\t"
                                    + "genes_exclusive:" + str(genes_exclusive) + "\t"
                                    + "number_genotypes:" + str(number_genotypes) + "\t"
                                    + "n_sample:" + str(n_sample) + "\n")
            
            #write_output_pan.write(str(number_genotypes) + "\t" + str(pan_transcriptome_size) + "\t" + "pan_transcriptome_size" + "\n")
            #write_output_core.write(str(number_genotypes) + "\t" + str(core_transcriptome_size) + "\t" + "core_transcriptome_size" + "\n")
            #write_output_accessory.write(str(number_genotypes) + "\t" + str(accessory_transcriptome_size) + "\t" + "accessory_transcriptome_size" + "\n")
            #write_output_exclusive.write(str(number_genotypes) + "\t" + str(exclusive_transcriptome_size) + "\t" + "exclusive_transcriptome_size" +" \n")

import pandas as pd
import numpy as np
from math import factorial
import sys

sys.setrecursionlimit(10**6)

data = pd.read_csv("aOrthogroups.GeneCount.tsv", delimiter='\t', header=0, index_col=0)
#max_n_sample = 20

print(data.shape)

def sample_random_selection(data, samples):
    my_sample = data.sample(number_genotypes, axis='columns', replace=False)
    
    my_selection = sorted(list(my_sample.columns))
    #print(f"sample dentro da funcao: {samples}, my_selection: {my_selection}; my_sample columns: {sorted(list(my_sample.columns))}")
    if my_selection in samples:
        sample_random_selection(data, samples)
    else:
        samples.append(my_selection)
    return(my_sample, samples)

for number_genotypes in range(1, data.shape[1]-1):
    max_n_sample = 20
    #print(number_genotypes)
    samples = []

    max_number_of_samples = int(factorial(data.shape[1]) / factorial((data.shape[1] - number_genotypes)))
    if max_number_of_samples < max_n_sample:
        max_n_sample = max_number_of_samples
    #print(max_n_sample)
    for n_sample in range(0, max_n_sample):
        pan_transcriptome_size = 0 
        core_transcriptome_size = 0
        #print(f"samples: {samples}; n_sample: {n_sample}" )
        my_sample,samples = sample_random_selection(data, samples)
        my_sample = np.array(my_sample)
        #print(f'number genotypes: {number_genotypes}; sample number: {n_sample}; genotypes: {list(my_sample.columns)}')
        #print(my_sample)

        for orthogroup in my_sample:
            number_of_genotypes_in_orthogroups = 0
            if sum(orthogroup) > 0:
                #number_of_genotypes_in_orthogroups += 1
                pan_transcriptome_size += 1
            for genotype in orthogroup:
                
                if genotype > 0:
                    number_of_genotypes_in_orthogroups += 1
                    
            if number_of_genotypes_in_orthogroups / number_genotypes > 0.9:
                core_transcriptome_size += 1
                
        print(f"pan_transcriptome_size: {pan_transcriptome_size};\t core_transcriptome_size: {core_transcriptome_size};\t number_genotypes: {number_genotypes}\t; n_sample: {n_sample}")
            
            
      
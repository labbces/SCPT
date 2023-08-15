#!/usr/bin/env python3

import pandas as pd
import numpy as np
from math import factorial
import sys
import argparse
import os.path
from matplotlib import markers, style
from matplotlib import pyplot as plt
import seaborn as sns

# creating arguments
parser = argparse.ArgumentParser(prog = "extractPanTranscriptomeGroups", description="Extract pan, hard-core, soft-core, accessory, and exclusives orthogroups from GeneCount.tsv file generated by OrthoFinder2", add_help=True)
parser.add_argument("-i", dest="input_file", metavar="<Orthogroups.GeneCount.tsv>", help="OrthoFinde2r GeneCount output", required=True)
parser.add_argument("-p", dest="min_fraction", type=float, help="Minimum fraction of genotypes to be present to consider a group as sort-core", default=0.9)

# getting arguments
args = parser.parse_args()
input_file = args.input_file
min_fraction=args.min_fraction
output_file = "Pan-Transcriptome_Size_" + str(min_fraction) + "." + os.path.basename(input_file)
output_pan = "Pan-Transcriptome_Size_" + str(min_fraction) + "." + os.path.basename(input_file)
output_core = "Core-Transcriptome_Size_" + str(min_fraction) + "." + os.path.basename(input_file)
output_accessory = "Accessory-Transcriptome_Size_" + str(min_fraction) + "." + os.path.basename(input_file)
output_exclusive = "Exclusive-Transcriptome_Size_" + str(min_fraction) + "." + os.path.basename(input_file)
outfigure_Groups_pdf="Pan-Transcriptome_Trajectory_Groups_" + str(min_fraction) + "." + os.path.basename(input_file) + ".pdf"
outfigure_Groups_png="Pan-Transcriptome_Trajectory_Groups_" + str(min_fraction) + "." + os.path.basename(input_file) + ".png"
outfigure_Genes_pdf="Pan-Transcriptome_Trajectory_Genes_" + str(min_fraction) + "." + os.path.basename(input_file) + ".pdf"
outfigure_Genes_png="Pan-Transcriptome_Trajectory_Genes_" + str(min_fraction) + "." + os.path.basename(input_file) + ".png"

# setting recursion limit to 1000000
sys.setrecursionlimit(10**6)

data = pd.read_csv(input_file, delimiter='\t', header=0, index_col=0)

print(f'The dimensions of the input dataset are: {data.shape}')
if 'Total' in data.columns:
    sys.stderr.write("The input data has a column names \"Total\", this is not expected and can generate some problems. Column will be removed!")
    data.drop('Total', axis=1, inplace=True)
    print(f'The dimensions of the input dataset, after removing the Total column, are: {data.shape}')

print(f'The dimensions of the input dataset, after removing the Total column, are: {data.shape}')

def sample_random_selection(data, samples):
    my_sample = data.sample(number_genotypes, axis='columns', replace=False)
    
    my_selection = sorted(list(my_sample.columns))
    #print(f"sample dentro da funcao: {samples}, my_selection: {my_selection}; my_sample columns: {sorted(list(my_sample.columns))}")
    if my_selection in samples:
        sample_random_selection(data, samples)
    else:
        samples.append(my_selection)
    return(my_sample, samples)

with open(output_file, "w") as write_output_file:
#    write_output_file.write("pan_transcriptome_size\tgenes_pan\thard_core_transcriptome_size\tgenes_hard_core\tsoft_core_transcriptome_size\tgenes_soft_core\taccessory_transcriptome_size\tgenes_accessory\texclusive_transcriptome_size\tgenes_exclusive\tnumber_genotypes\tn_sample\n")
    write_output_file.write("NumberGroups\tNumberGenes\tClassification\tNumberGenotypes\tSample\n")

    for number_genotypes in range(1, data.shape[1]):
        max_n_sample = 20
        #print(number_genotypes)
        samples = []

        max_number_of_samples = int(factorial(data.shape[1]) / factorial((data.shape[1] - number_genotypes)))
        if max_number_of_samples < max_n_sample:
            max_n_sample = max_number_of_samples
        #print(max_n_sample)

        for n_sample in range(0, max_n_sample):
            pan_transcriptome_size = 0
            genes_pan = 0
            hard_core_transcriptome_size = 0
            soft_core_transcriptome_size = 0
            accessory_transcriptome_size = 0
            exclusive_transcriptome_size = 0
            genes_hard_core = 0
            genes_soft_core = 0
            genes_accessory = 0
            genes_exclusive = 0
            #print(f"samples: {samples}; n_sample: {n_sample}" )
            my_sample,samples = sample_random_selection(data, samples)
            my_sample = np.array(my_sample)
            #print(f'number genotypes: {number_genotypes}; sample number: {n_sample}; genotypes: {list(my_sample.columns)}')
            #print(my_sample)

            for orthogroup in my_sample:
                number_of_genotypes_in_orthogroups = 0
#                print(f'{n_sample} {orthogroup}')  
                if sum(orthogroup) > 0:
                    genes_pan += sum(orthogroup)
                    pan_transcriptome_size += 1
                    for genotype in orthogroup:
                        if genotype > 0:
                            number_of_genotypes_in_orthogroups += 1

                    proporcao = number_of_genotypes_in_orthogroups / number_genotypes
                    if proporcao >= min_fraction:
                        genes_soft_core += sum(orthogroup)
                        soft_core_transcriptome_size += 1
                        if number_of_genotypes_in_orthogroups == number_genotypes:
                            genes_hard_core += sum(orthogroup)
                            hard_core_transcriptome_size += 1
                    elif number_of_genotypes_in_orthogroups > 1 and proporcao < min_fraction:
                        genes_accessory += sum(orthogroup)
                        accessory_transcriptome_size += 1
                    elif number_of_genotypes_in_orthogroups == 1:
                        genes_exclusive += sum(orthogroup)
                        exclusive_transcriptome_size += 1
                    else:
                        print("Case not contemplated, check input\n")

            #print(f"pan_transcriptome_size: {pan_transcriptome_size} \t core_transcriptome_size: {core_transcriptome_size} \t number_genotypes: {number_genotypes} \t n_sample: {n_sample}")

#            write_output_file.write(str(pan_transcriptome_size) + "\t"
#                                    + str(genes_pan) + "\t"
#                                    + str(hard_core_transcriptome_size) + "\t"
#                                    + str(genes_hard_core) + "\t"
#                                    + str(soft_core_transcriptome_size) + "\t"
#                                    + str(genes_soft_core) + "\t"
#                                    + str(accessory_transcriptome_size) + "\t"
#                                    + str(genes_accessory) + "\t"
#                                    + str(exclusive_transcriptome_size) + "\t"
#                                    + str(genes_exclusive) + "\t"
#                                    + str(number_genotypes) + "\t"
#                                    + str(n_sample) + "\n")
            write_output_file.write(str(pan_transcriptome_size)+ "\t"
                                    + str(genes_pan) + "\t"
                                    + "Pan-transcriptome" + "\t"
                                    + str(number_genotypes) + "\t"
                                    + str(n_sample) + "\n"
                                    + str(hard_core_transcriptome_size) + "\t"
                                    + str(genes_hard_core) + "\t"
                                    + "Hard-Core-transcriptome" + "\t"
                                    + str(number_genotypes) + "\t"
                                    + str(n_sample) + "\n"
                                    + str(soft_core_transcriptome_size) + "\t"
                                    + str(genes_soft_core) + "\t"
                                    + "Soft-Core-transcriptome" + "\t"
                                    + str(number_genotypes) + "\t"
                                    + str(n_sample) + "\n"
                                    + str(accessory_transcriptome_size) + "\t"
                                    + str(genes_accessory) + "\t"
                                    + "Acc-transcriptome" + "\t"
                                    + str(number_genotypes) + "\t"
                                    + str(n_sample) + "\n"
                                    + str(exclusive_transcriptome_size) + "\t"
                                    + str(genes_exclusive) + "\t"
                                    + "Exc-transcriptome" + "\t"
                                    + str(number_genotypes) + "\t"
                                    + str(n_sample) + "\n")



data = pd.read_csv(output_file, delimiter="\t")
plt.figure(figsize=(20,13))
pan_trajectory_groups=sns.lineplot(y="NumberGroups", x = "NumberGenotypes", data = data, hue="Classification",marker="o", alpha=0.3, palette="tab10")
fig1 = pan_trajectory_groups.get_figure()
fig1.savefig(outfigure_Groups_png)
fig1.savefig(outfigure_Groups_pdf,format='pdf') 
plt.figure(figsize=(20,13))
pan_trajectory_genes=sns.lineplot(y="NumberGenes", x = "NumberGenotypes", data = data, hue="Classification",marker="o", alpha=0.3, palette="tab10")
fig2 = pan_trajectory_genes.get_figure()
fig2.savefig(outfigure_Genes_png) 
fig2.savefig(outfigure_Genes_pdf,format='pdf') 



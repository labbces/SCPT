#!/bin/bash

#$ -q all.q
#$ -V
#$ -cwd
#$ -t 1-17
#$ -tc 5
#$ -pe smp 1

GENOTYPE=`ls -1 dataset/MyAssembly_* | head -n $SGE_TASK_ID | tail -n 1 | awk -F "_" '{print $2}'`

echo MyAssembly_${GENOTYPE}_fasta_str1_l50_E1e-05.diamond.cds.faa
echo mod_MyAssembly_${GENOTYPE}_fasta_str1_l50_E1e-05.diamond.cds.faa

sed -e "s/>/>${GENOTYPE}_/ ; s/*/X/g" dataset/MyAssembly_${GENOTYPE}_fasta_str1_l50_E1e-05.diamond.cds.faa > mod_MyAssembly_${GENOTYPE}_fasta_str1_l50_E1e-05.diamond.cds.faa

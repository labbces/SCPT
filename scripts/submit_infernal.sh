#!/bin/bash

#$ -q all.q
#$ -V
#$ -cwd
#$ -t 1-32
#$ -tc 10
#$ -pe smp 1

transcriptome=`ls -1 datasets/*.fa | head -n $SGE_TASK_ID | tail -n1`
transcriptome_base=`basename $transcriptome`
genotype=${transcriptome_base/.fa}
clanin=rfam_files/Rfam.clanin
cm=rfam_files/Rfam.cm

module load infernal/1.1.2

echo $transcriptome
echo $genotype

/usr/bin/time -v cmscan --nohmmonly --rfam --cut_ga --fmt 2 --oclan --oskip --clanin $clanin -o ${genotype}.cmscan.out --tblout ${genotype}.cmscan.tblout $cm $transcriptome

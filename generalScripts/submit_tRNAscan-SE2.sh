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

module load tRNAscan-SE/2.0

/usr/bin/time -v tRNAscan-SE -o ${genotype}.trnas -m ${genotype}.stats $transcriptome

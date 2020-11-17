#!/bin/bash

#$ -cwd
#$ -V
#$ -q all.q
#$ -pe smp 1

infileR1=`ls -1 *.trimmed.R1.fastq* | head -n $SGE_TASK_ID | tail -n1`
infileR2=${infileR1/1.fastq/2.fastq}

module load miniconda2
time ./create_fastq_indexdb.py -R1 $infileR1 -R2 $infileR2

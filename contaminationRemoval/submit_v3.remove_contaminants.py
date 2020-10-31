#!/bin/bash
#$ -cwd
#$ -V
#$ -q all.q
#$ -t 1-26
#$ -pe smp 1


kaiju_file=`ls -1 *.kaiju`
infileR1=`ls -1 *R1.fastq* | head -n $SGE_TASK_ID | tail -n1`
infileR2=${infileR1/1.fastq/2.fastq}

module load miniconda2
time ./v3.remove_contaminants.py -k kaiju_file -R1 $infileR1 -R2 $infileR2 -t Viridiplantae


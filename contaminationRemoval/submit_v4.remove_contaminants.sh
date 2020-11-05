#!/bin/bash
#$ -cwd
#$ -V
#$ -q all.q
#$ -t 1-9
#$ -pe smp 1

infileR1=`ls -1 *.trimmed.R1.fastq* | head -n1 | tail -n1`
infileR2=${infileR1/1.fastq/2.fastq}
kaiju=`ls -1 *.kaiju | head -n $SGE_TASK_ID | tail -n1`

module load miniconda2
time ./v4.remove_contaminants.py -k $kaiju -R1 $infileR1 -R2 $infileR2 -t Viridiplantae

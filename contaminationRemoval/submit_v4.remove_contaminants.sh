#!/bin/bash
#$ -cwd
#$ -V
#$ -q all.q
#$ -t 1-26
#$ -pe smp 1


#SRR8771429.trimmed.5905288_00_R1.fastq
infileR1=`ls -1 *.trimmed.R1.fastq* | head -n1 | tail -n1`
infileR2=${infileR1/1.fastq/2.fastq}
kaiju=`ls -1`

module load miniconda2
time ./v3.remove_contaminants.py -k SRR8771429.trimmed.kaiju -R1 $infileR1 -R2 $infileR2 -t Viridiplantae


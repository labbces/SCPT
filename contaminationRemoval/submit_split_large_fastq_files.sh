#!/bin/bash

#$ -cwd
#$ -V
#$ -q all.q
#$ -t 1
#$ -pe smp 1

R1_file=`ls -1 *R1*`
R2_file=${R1_file/R1.fastq/R2.fastq}

#echo $R1_file
#echo $R2_file

split -l 5905288 -d --additional-suffix=_R1.fastq  $R1_file SRR8771429.trimmed.5905288_
split -l 5905288 -d --additional-suffix=_R2.fastq  $R2_file SRR8771429.trimmed.5905288_

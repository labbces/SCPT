#!/bin/bash

#$ -cwd
#$ -V
#$ -q all.q
#$ -t 1-2
#$ -pe smp 1

fastq_file=`ls -1 *R1.fastq | head -n $SGE_TASK_ID | tail -n1`
outbase=`basename $fastq_file`
prefix=${outbase/.trimmed.R1.fastq/.trimmed_}
kaiju=`ls -1 *.trimmed.kaiju | head -n $SGE_TASK_ID | tail -n1`

split -l 4069754 -d --additional-suffix=.kaiju $kaiju $prefix

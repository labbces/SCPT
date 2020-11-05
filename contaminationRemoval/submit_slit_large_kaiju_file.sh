#!/bin/bash

#$ -cwd
#$ -V
#$ -q all.q
#$ -t 1
#$ -pe smp 1

fastq_file=`ls -1 *R1*`
outbase=`basename $fastq_file`
prefix=${outbase/.trimmed.R1.fastq}
kaiju=`ls -1 *.trimmed.kaiju`

echo $prefix

split -n 8 -d --additional-suffix=.kaiju  $kaiju $prefix.trimmed_

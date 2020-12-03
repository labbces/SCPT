#!/bin/bash

#$ -cwd
#$ -V
#$ -q all.q
#$ -t 1
#$ -pe smp 1

fastq_file=`ls -1 *R1*`
outbase=`basename $fastq_file`
prefix=${outbase/.trimmed.R1.fastq}
kaiju=`ls -1 *.trimmed.kraken`

split -l 5331149 -d --additional-suffix=.kraken  $kaiju $prefix.trimmed_

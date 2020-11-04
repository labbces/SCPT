#!/bin/bash

#$ -cwd
#$ -V
#$ -q all.q
#$ -t 1
#$ -pe smp 1

#SRR8771429.trimmed.kaiju
kaiju=`ls -1 *.trimmed.kaiju`

split -l 2952644 -d --additional-suffix=.kaiju  $R1_file SRR8771429.trimmed.2952644_

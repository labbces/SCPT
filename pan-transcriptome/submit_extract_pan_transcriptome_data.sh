#!/bin/bash

#$ -q all.q
#$ -V
#$ -cwd
#$ -pe smp 1

INFILE=43_Orthogroups.GeneCount.tsv

module load Python/3.7.2
/usr/bin/time -v python3.7 extract_pan_transcriptome_data.py -i ${INFILE}

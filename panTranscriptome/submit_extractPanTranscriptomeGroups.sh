#!/bin/bash

#$ -q all.q
#$ -V
#$ -cwd
#$ -pe smp 1

INFILE=Pan-Transcriptome_Size.Orthogroups.GeneCount_I1.5_v1.tsv

module load Python/3.7.2
/usr/bin/time -v python3.7 extractPanTranscriptomeGroups.py -i ${INFILE}

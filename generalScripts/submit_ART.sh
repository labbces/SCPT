#!/bin/bash

#$ -cwd
#$ -V
#$ -q all.q
#$ -pe smp 8

./art_illumina -d SP80-3280 -ss HS20 -i Riano-Pachon_2017_Illumina_Genome.fasta -p -l 100 -f 10 -m 150 -s 10 -o SP80-3280_synthetic


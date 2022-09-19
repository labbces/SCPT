#!/bin/bash

#$ -q all.q
#$ -V
#$ -cwd
#$ -pe smp 4

#Define output path
OUT=/Storage/data1/felipe.peres/Sugarcane/rawReads/MyAssembly

#Loading sratoolkit
module load sratoolkit/2.9.6 

#Read SRR_Accession.txt and do prefetch to download files by their SRR ID
cat SRR_Accession.txt | while read line; do (prefetch ${line} -O $OUT/1_raw_reads_in_sra_format); done

#!/bin/bash

#$ -q all.q
#$ -V
#$ -cwd
#$ -pe smp 4
#$ -t 1-4
#$ -tc 4 


#Getting SRA file names
SRA=`ls -1 *.sra|head -n $SGE_TASK_ID|tail -n1`

#Define output path
OUT=/Storage/data1/felipe.peres/Sugarcane/rawReads/MyAssembly_Banerjee_2019_Illumina/2_raw_reads_in_fastq_format

#Loading sratoolkit
module load sratoolkit/2.9.6

#Split SRA files into R1.fastq and R2.fastq
fastq-dump --defline-seq '@$sn[_$rn]/$ri' --split-files $SRA -O $OUT

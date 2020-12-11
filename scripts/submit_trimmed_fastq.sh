#!/bin/bash

#$ -q all.q
#$ -V
#$ -cwd
#$ -pe smp 4
#$ -t 1-8
#$ -tc 4

#Define output path
OUT=/Storage/data1/felipe.peres/Sugarcane/rawReads/MyAssembly_Banerjee_2019_Illumina
FASTAFILE=`ls -1 /Storage/data1/felipe.peres/Sugarcane/rawReads/MyAssembly_Banerjee_2019_Illumina/4_trimmed_reads/*.fastq|head -n $SGE_TASK_ID|tail -n1`
OUTPUT=${OUT}/5_trimmed_reads_fastqc_reports

#Loading FastQC
module load FastQC/0.11.8
fastqc -f fastq -o ${OUTPUT} ${FASTAFILE}

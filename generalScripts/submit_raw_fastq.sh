#!/bin/bash
#$ -q all.q
#$ -V
#$ -cwd
#$ -pe smp 4
#$ -t 1-8
#$ -tc 4

#Define output path
OUT=/Storage/data1/felipe.peres/Sugarcane/rawReads/MyAssembly_Banerjee_2019_Illumina

#Getting fastq filenames 
FASTQFILE=`ls -1 /Storage/data1/felipe.peres/Sugarcane/rawReads/MyAssembly_Banerjee_2019_Illumina/2_raw_reads_in_fastq_format/*.fastq|head -n $SGE_TASK_ID|tail -n1`
OUTPUT=${OUT}/3_raw_reads_fastqc_reports

#Loading FastQC
module load FastQC/0.11.8
fastqc -f fastq ${FASTQFILE} -o ${OUTPUT}

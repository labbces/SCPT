#!bin/bash

#$ -q all.q
#$ -V
#$ -cwd
#$ -pe smp 2

#Loading salmon
module load salmon/1.3.0

R1=`ls -1 SRR8771429.trimmed.filtered.total.R1.fastq`
R2=${R1/.R1.fastq/.R2.fastq}

/usr/bin/time -v salmon quant -i salmon_index_v2 -l A -1 $R1 -2 $R2 --validateMappings -o transcripts_quant


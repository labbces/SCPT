#!/bin/bash

#$ -q all.q
#$ -V
#$ -cwd
#$ -pe smp 10
#$ -l h=figsrv

INFILER1=`ls -1 /Storage/data1/felipe.peres/Sugarcane/rawReads/MyAssembly_Banerjee_2019_Illumina/4_trimmed_reads/MS6847/SRR8771429.trimmed.R1.fastq |head -n1 | tail -n 1`
INFILER2=${INFILER1/trimmed.R1.fastq/trimmed.R2.fastq}
OUTBASE=`basename $INFILER1`
OUTBASE=${OUTBASE/.trimmed.R1.fastq}
OUTPUT=${OUTBASE}.trimmed.kraken

module load Kraken2/2.0.7_beta
kraken2 --db /Storage/data1/felipe.peres/kraken2/KrakenDB --threads $NSLOTS --report-zero-counts --report --output $OUTPUT --paired $INFILER1 $INFILER2

#!/bin/bash

#$ -q all.q
#$ -V
#$ -cwd
#$ -pe smp 2

ASSEMBLY=/Storage/data1/felipe.peres/Sugarcane/rawReads/MyAssembly_Banerjee_2019_Illumina/9_trinity_assembly/CoV92102
REF=/Storage/data1/felipe.peres/Sugarcane/rawReads/MyAssembly_Banerjee_2019_Illumina/11_transrate_assembly/transrate_references/Sbicolor_454_v3.1.1.transcript.fa
OUT=transrate_comparative_merged_transcriptome_contig_min_lenght301

#Loading TRANSRATE
module load transrate/1.0.3
/usr/bin/time -v transrate --assembly $ASSEMBLY/MyAssembly_CoV92102_trinity_k25_and_k31.Trinity.merged.final_gt301bp.fasta --reference $REF --threads $NSLOTS --output $OUT


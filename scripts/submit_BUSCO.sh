#!/bin/bash

#$ -q all.q
#$ -V
#$ -cwd
#$ -pe smp 2

#Getting assembly filename
FASTAFILE=`ls -1 /Storage/data1/felipe.peres/Sugarcane/rawReads/MyAssembly_Banerjee_2019_Illumina/9_trinity_assembly/CoV92102/MyAssembly_CoV92102_trinity_k25_and_k31.Trinity.merged.final_gt301bp.fasta`
OUTFILE=MyAssembly_CoV92102_trinity_k25andk31_busco

#Loading BUSCO
module load BUSCO/3.0

/usr/bin/time -v run_BUSCO.py -i $FASTAFILE -o $OUTFILE -c $NSLOTS -m transcriptome -l /Storage/databases/BUSCO_DBs/embryophyta_odb9/

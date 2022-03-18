#!/bin/bash

#$ -q all.q
#$ -V
#$ -cwd
#$ -t 1
#$ -tc 1
#$ -pe smp 1

transcriptome=`ls -1 datasets/*.fa | head -n1 | tail -n1`
transcriptome_base=`basename $transcriptome`
genotype=${transcriptome_base/.fa}

module load RNAmmer/1.2

/usr/bin/time -v rnammer -S euk -gff ${genotype}_out_gff -multi -m tsu,ssu,lsu -h ${genotype}_out_hmm -f ${genotype}_out_fasta $transcriptome


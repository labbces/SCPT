#!/bin/bash

#$ -cwd
#$ -q all.q
#$ -pe smp 20

uniref90=/Storage/data1/felipe.peres/UniRef90/uniref90.dmnd

module load Diamond/0.9.24

/usr/bin/time -v diamond blastp --query ./../32GenotypesMerged.fasta_str1_l50_E1e-05.diamond.cds.faa --db $uniref90 --threads $NSLOTS --max-target-seqs 6 --outfmt 6 --more-sensitive --evalue 1e-3 >> ./../results/diamondP_32Genotypes_uniref90.outfmt6.full.ok

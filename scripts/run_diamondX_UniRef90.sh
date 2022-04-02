#!/bin/bash

#$ -cwd
#$ -q all.q
#$ -pe smp 10

uniref90=/Storage/data1/felipe.peres/UniRef90/uniref90.dmnd

module load Diamond/0.9.24

/usr/bin/time -v diamond blastx --query ./../5GenotypesMerged.fasta --db $uniref90 --threads $NSLOTS --max-target-seqs 6 --outfmt 6 --more-sensitive --evalue 1e-3 >> ./../results/diamondX_5Genotypes_uniref90.outfmt6.full.ok

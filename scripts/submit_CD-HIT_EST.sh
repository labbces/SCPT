#!/bin/bash

#$ -q all.q
#$ -V
#$ -cwd
#$ -pe smp 1

#Getting genotype name
GENOTYPE=`ls -1 MyAssembly* | head -n1 | tail -n1 | awk -F "_" '{print $2}'`

#Add identification to assembled sequences
sed 's/>/>k25_/' MyAssembly_${GENOTYPE}_trinity_k25.Trinity.fasta > MyAssembly_${GENOTYPE}_trinity_k25.Trinity.mod.fasta
sed 's/>/>k31_/' MyAssembly_${GENOTYPE}_trinity_k31.Trinity.fasta > MyAssembly_${GENOTYPE}_trinity_k31.Trinity.mod.fasta
cat MyAssembly_${GENOTYPE}_trinity_k25.Trinity.mod.fasta MyAssembly_${GENOTYPE}_trinity_k31.Trinity.mod.fasta > MyAssembly_${GENOTYPE}_trinity_k25_and_k31.Trinity.merged.mod.fasta

#Loading CD-HIT
module load CD-HIT/4.8.1

#Running CD-HIT_EST and generate clustered assembly (kmer25 + kmer31)
/usr/bin/time -v cd-hit-est -i MyAssembly_${GENOTYPE}_trinity_k25_and_k31.Trinity.merged.mod.fasta -o MyAssembly_${GENOTYPE}_trinity_k25_and_k31.Trinity.merged.final.fasta -c 1 -n 11 -T $NSLOTS -M 0 -d 0 -r 0 -g 1

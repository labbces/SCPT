#!/bin/bash

#$ -q all.q
#$ -V
#$ -cwd
#$ -t 1
#$ -pe smp 8

module load mcl/14-137
module load Diamond/0.9.24
module load OrthoFinder/2.3.3

#First run
#/usr/bin/time -v orthofinder -f proteomes -t $NSLOTS -a $NSLOTS

#Add new species in <dir1> to previous run in <dir2> and run new analysis
/usr/bin/time -v orthofinder -f proteomes_ultima_adicao -b proteomes_total/OrthoFinder/Results_Jan05/WorkingDirectory -t $NSLOTS -a $NSLOTS

#Run after RAM issues. Changes: removed '-a' and '-f', added '-fg' to start OrthoFinder from pre-computed orthogroups
#/usr/bin/time -v orthofinder -fg /Storage/data1/felipe.peres/Sugarcane/CD_HIT/pep/CD_HIT_perGenotype/proteomes/OrthoFinder/Results_Aug17/ -t $NSLOTS


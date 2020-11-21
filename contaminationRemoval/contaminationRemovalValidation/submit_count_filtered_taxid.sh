#!/bin/bash

#$ -q all.q
#$ -cwd
#$ -V
#$ -pe smp 1

kraken=`ls *filtered* | head -n1 | tail -n1`

time ./count_taxid.py -k $kraken -t Viridiplantae

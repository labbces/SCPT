#!/bin/bash

#$ -q all.q
#$ -V
#$ -cwd
#$ -pe smp 1

module load R/4.0.0
/usr/bin/time -v Rscript GO_enrichment.R
echo End of GO enrichment analysis !

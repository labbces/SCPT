#!/bin/bash

#$ -q all.q
#$ -V
#$ -cwd
#$ -t 1-48
#$ -tc 10
#$ -pe smp 1

transcriptome=`ls -1 *.stats | head -n $SGE_TASK_ID | tail -n1`

tail -n 23 $transcriptome | cut -f1 > temp_${transcriptome}

cut -d ":" -f2 temp_${transcriptome} > tRNAs_${transcriptome}

rm temp_${transcriptome}

cat tRNAs_${transcriptome} | cut -d " " -f2 | tr '\n' ',' >> heatmap_tRNAs.csv

rm tRNAs_${transcriptome}

sed 's/,,/\n/g' heatmap_tRNAs.csv > heatmap_final_48_tRNAs.csv

rm heatmap_tRNAs.csv

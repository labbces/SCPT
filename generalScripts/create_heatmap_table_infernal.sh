#!/bin/bash

#$ -q all.q
#$ -V
#$ -cwd
#$ -t 1-48
#$ -tc 10
#$ -pe smp 1

genotype=`ls -1 *.tblout | awk -F "_" '{print $3}' | head -n $SGE_TASK_ID | tail -n1`
create_temp=`awk 'NR>2{printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" ,$1,$2,$3,$4,$6,$10,$11,$12,$18,$20}' mod_MyAssembly_${genotype}_ncRNA.cmscan.tblout > temp_mod_MyAssembly_${genotype}_ncRNA.cmscan.tblout`

temp_tblout=`ls -1 temp_mod_MyAssembly_${genotype}_ncRNA.cmscan.tblout`

#Contar Small Nuclear RNA (sno)
sno=`cut -f2 $temp_tblout | grep -i "^sno" | wc -l`

#Contar RNA transportador (tRNA)
trna=`cut -f2 $temp_tblout | grep -i "^trna" | wc -l`

#Contar micro RNA (mir)
mir=`cut -f2 $temp_tblout | grep -i "^mir" | wc -l`

#Contar intron_gp
intron_gp=`cut -f2 $temp_tblout | grep -i "^intron" | wc -l`

#Contar U
u=`cut -f2 $temp_tblout | grep -i "^u" | wc -l`

#Contar TPP
tpp=`cut -f2 $temp_tblout | grep -i "^tpp" | wc -l`

#Contar enod
enod=`cut -f2 $temp_tblout | grep -i "^enod" | wc -l`

echo $genotype,$sno,$trna,$mir,$intron_gp,$u,$tpp,$enod >> heatmap_48_table.csv

rm $temp_tblout

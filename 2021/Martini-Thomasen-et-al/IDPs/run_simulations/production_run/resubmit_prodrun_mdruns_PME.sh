#!/bin/bash 
 
for i in aSyn_PME Hst5_PME
do 
 
cd $i 
 
for j in 1.00 1.04 1.06 1.08 1.10 1.12 1.14
do 
 
cd lambda_${j} 
 
qsub prodrun_mdrun.sh
cd .. 
 
done 
 
cd .. 
 
done 
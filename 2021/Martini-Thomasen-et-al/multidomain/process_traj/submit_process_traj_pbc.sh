#!/bin/bash

for i in hSUMO_hnRNPA1 hnRNPA1 TIA1
do

cd $i

for j in 1.00 1.02 1.04 1.06 1.08 1.10 1.12 1.14
do

cd lambda_${j}
cp ../../process_traj_pbc.sh .
qsub process_traj_pbc.sh
rm \#*
cd ..

done

cd ..

done


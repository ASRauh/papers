#!/bin/bash

for i in Hst5_PME aSyn_PME
do

cd $i

if [[ "$i" == "Hst5_PME" || "$i" == "aSyn_PME" ]]
then
        t=293
fi

echo "$i is at ${t}K"

for j in 1.00 1.04 1.06 1.08 1.10 1.12 1.14
do

mkdir lambda_$j
cd lambda_$j
cp ../../relax_grompp_PME.sh .
cp ../all_PRO_lambda${j}.top .
mv all_PRO_lambda${j}.top all_PRO_lambda.top
qsub relax_grompp_PME.sh -v temp=$t
cd ..

done

cd ..

done

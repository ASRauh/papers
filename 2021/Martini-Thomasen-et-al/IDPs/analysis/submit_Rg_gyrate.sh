#!/bin/bash

for i in K25 A1 CoRNID ColNT FhuA Hst52 K19 PNt Sic1 aSyn Hst5 ACTR ACTR_helices aSyn_bigboxtest aSyn_PME Hst5_PME
do

cd $i

for j in 1.00 1.04 1.06 1.08 1.10 1.12 1.14
do

cd lambda_${j}
cp ../../make_Rg_gyrate.sh .
qsub make_Rg_gyrate.sh
rm \#*

cd ..

done

cd ..

done


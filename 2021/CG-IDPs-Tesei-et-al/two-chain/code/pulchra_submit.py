import os
import subprocess
import time
from jinja2 import Template
from analyse import *

proteins = initProteinsDimers()
proteins.to_pickle('proteins.pkl')

submission = Template("""#!/bin/bash
#SBATCH --job-name=PULCHRA{{ff}}
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=64
#SBATCH --exclusive
#SBATCH --threads-per-core=1
#SBATCH --mem-per-cpu=2000
#SBATCH -t 20:00:00
#SBATCH -o p_{{ff}}_{{run}}.out
#SBATCH -e p_{{ff}}_{{run}}.err
#SBATCH --partition=sbinlab

source /groups/sbinlab/giulio/.bashrc
conda activate hoomd

echo $SCRATCH

cp *.py $SCRATCH
cp proteins.pkl $SCRATCH
mkdir $SCRATCH/{{name}}
mkdir $SCRATCH/{{name}}/{{ff}}
cp -r {{name}}/{{ff}}/run{{run}} $SCRATCH/{{name}}/{{ff}}

echo $SLURM_CPUS_PER_TASK

cd $SCRATCH

start=$(date +%s.%N)

python ./pulchra.py --name {{name}} --num_cpus $SLURM_CPUS_PER_TASK --ff {{ff}} --run {{run}} --pulchra /groups/sbinlab/giulio/pulchra_306/pulchra

cp -r {{name}}/{{ff}}/run{{run}}/* $SLURM_SUBMIT_DIR/{{name}}/{{ff}}/run{{run}}

duration=$(echo "$(date +%s.%N) - $start" | bc)
execution_time=`printf "%.2f seconds" $duration`

echo $execution_time""")

for name in ['A2','FUS']:
    for i in [1,2,3]:
        for k in [10]:
            with open('p_{:s}_{:d}{:d}.sh'.format(name,i,k), 'w') as submit:
                submit.write(submission.render(name=name,ff='M{:d}'.format(i),run=k))
            subprocess.run(['sbatch','--partition','sbinlab','p_{:s}_{:d}{:d}.sh'.format(name,i,k)])
            time.sleep(2)

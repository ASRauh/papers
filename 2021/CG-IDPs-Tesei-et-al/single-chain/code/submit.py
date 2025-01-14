import pandas as pd
import os
import subprocess
from jinja2 import Template

submission = Template("""#!/bin/bash
#SBATCH --job-name={{name}}
#SBATCH --nodes=1           
#SBATCH --partition=sbinlab
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --ntasks=1
#SBATCH -t 16:00:00
#SBATCH -o {{name}}.out
#SBATCH -e {{name}}.err
#SBATCH --mem-per-cpu=2000

source /groups/sbinlab/giulio/.bashrc
conda activate hoomd

python ./simulate.py --name {{name}} --model {{model}}""")

def initProteins():
    proteins = pd.DataFrame(index=['A1','A1NLS','NEWSEQ'],
            columns=['temp','pH','ionic','fasta'])
    fasta_A1 = """GSMASASSSQRGRSGSGNFGGGRGGGFGGNDNFGRGGNFSGRGGFGGSRGGGGYGGSGDGYNGFGNDGSNFGGGGSYNDFGNYNNQ
SSNFGPMKGGNFGGRSSGGSGGGGQYFAKPRNQGGYGGSSSSSSYGSGRRF""".replace('\n', '')
    fasta_A1NLS = """GSMASASSSQRGRSGSGNFGGGRGGGFGGNDNFGRGGNFSGRGGFGGSRGGGGYGGSGDGYNGFGNDGSNFGGGGSYNDFGNYNNQ
SSNFGPMKGGNFGGRSSGPYGGGGQYFAKPRNQGGYGGSSSSSSYGSGRRF""".replace('\n', '')
    fasta_NEWSEQ = """INSERT YOUR SEQUENCE HERE""".replace('\n', '')
    proteins.loc['A1'] = dict(temp=298,pH=7.0,fasta=list(fasta_A1),ionic=0.15)
    proteins.loc['A1NLS'] = dict(temp=298,pH=7.0,fasta=list(fasta_A1NLS),ionic=0.15)
    proteins.loc['NEWSEQ'] = dict(temp=298,pH=7.0,fasta=list(fasta_NEWSEQ),ionic=0.15)
    return proteins

proteins = initProteins()
proteins.to_pickle('proteins.pkl')

model = 'M1' # available models: 'M1', 'M2', 'M3', 'AVG', 'HPSUrry' and 'HPS'

for name in ['NEWSEQ']: # or proteins.index: to simulate all the sequences in initProteins()
    if not os.path.isdir(name):
        os.mkdir(name)
    with open('{:s}.sh'.format(name), 'w') as submit:
        submit.write(submission.render(name=name,model=model))
    subprocess.run(['sbatch','--partition','sbinlab','{:s}.sh'.format(name)])

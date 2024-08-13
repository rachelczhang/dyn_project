#!/bin/bash

#SBATCH -J testcosmic
#SBATCH --mail-user=rczhang@u.northwestern.edu
#SBATCH --error=testcosmicerr.out
#SBATCH --output=testcosmicoutput.out
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=28
#SBATCH --mem=50G
#SBATCH --time=00:20:00
#SBATCH --account=b1095
#SBATCH --partition=grail-std

source activate cosmic
python test_cosmic.py

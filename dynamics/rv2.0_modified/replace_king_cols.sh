#!/bin/bash

#SBATCH -J replace
#SBATCH --mail-user=rczhang@u.northwestern.edu
#SBATCH --error=replaceerror.out
#SBATCH --output=replaceoutput.out
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=100G
#SBATCH --time=00:30:00
#SBATCH --account=b1095
#SBATCH --partition=grail-std
source activate cosmic
python replace_king_cols.py

#!/bin/bash

#SBATCH -J run_bh
#SBATCH --mail-user=rczhang@u.northwestern.edu
#SBATCH --error=bh_err.out
#SBATCH --output=bh_output.out
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=15G
#SBATCH --time=00:10:00
#SBATCH --account=b1095
#SBATCH --partition=grail-std

source activate cosmic
python analyze_BHs.py

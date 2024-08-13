#!/bin/bash

#SBATCH -J escape2.0
#SBATCH --mail-user=rczhang@u.northwestern.edu
#SBATCH --error=escapereviseerr.out
#SBATCH --output=escapereviseout.out
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=28
#SBATCH --mem=50G
#SBATCH --time=10:00:00
#SBATCH --account=b1095
#SBATCH --partition=grail-std

source activate cosmic
python revised_run_escapers.py

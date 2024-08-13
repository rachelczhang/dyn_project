#!/bin/bash

#SBATCH -J escapecosmic
#SBATCH --mail-user=rczhang@u.northwestern.edu
#SBATCH --error=escapecosmicerr.out
#SBATCH --output=escapecosmicout.out
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=28
#SBATCH --mem=50G
#SBATCH --time=100:00:00
#SBATCH --account=b1095
#SBATCH --partition=grail-std

source activate cosmic
python run_escapers.py

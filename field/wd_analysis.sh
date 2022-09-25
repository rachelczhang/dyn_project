#!/bin/bash

#SBATCH -J wd_analysis
#SBATCH --mail-user=rczhang@u.northwestern.edu
#SBATCH --error=wderr.out
#SBATCH --output=wdoutput.out
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=28
#SBATCH --mem=50G
#SBATCH --time=200:00:00
#SBATCH --account=b1095
#SBATCH --partition=grail-std

source activate cosmic
python wd_analysis.py

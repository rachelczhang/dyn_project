#!/bin/bash

#SBATCH -J primordial
#SBATCH --mail-user=rczhang@u.northwestern.edu
#SBATCH --error=primerror.out
#SBATCH --output=primoutput.out
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=20G
#SBATCH --time=00:10:00
#SBATCH --account=b1094
#SBATCH --partition=ciera-std
source activate cosmic
python primordial_binaries.py

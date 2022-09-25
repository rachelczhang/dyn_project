#!/bin/bash

#SBATCH -J quickgenerate
#SBATCH --mail-user=rczhang@u.northwestern.edu
#SBATCH --error=error.out
#SBATCH --output=output.out
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=5G
#SBATCH --time=00:10:00
#SBATCH --account=b1095
#SBATCH --partition=grail-std
source activate cosmic
python generate_king_profile.py

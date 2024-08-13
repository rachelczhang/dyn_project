#!/bin/bash

#SBATCH -J analyzemodel
#SBATCH --mail-user=rczhang@u.northwestern.edu
#SBATCH --error=analyzemodelerror.out
#SBATCH --output=analyzemodeloutput.out
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=20G
#SBATCH --time=00:20:00
#SBATCH --account=b1095
#SBATCH --partition=grail-std
source activate cosmic
python analyze_models.py dynamics/rv2.0_modified/


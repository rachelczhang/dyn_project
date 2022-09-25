#!/bin/bash

#SBATCH -J init
#SBATCH --mail-user=rczhang@u.northwestern.edu
#SBATCH --error=initerror.out
#SBATCH --output=initoutput.out
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=20G
#SBATCH --time=00:10:00
#SBATCH --account=b1094
#SBATCH --partition=ciera-std
source activate cosmic
python compare_init_cond.py

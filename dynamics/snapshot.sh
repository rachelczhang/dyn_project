#!/bin/bash

#SBATCH -J snapshot
#SBATCH --mail-user=rczhang@u.northwestern.edu
#SBATCH --error=snapshoterror.out
#SBATCH --output=snapshotoutput.out
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=20G
#SBATCH --time=00:10:00
#SBATCH --account=b1095
#SBATCH --partition=grail-std
source activate cosmic
python snapshot.py

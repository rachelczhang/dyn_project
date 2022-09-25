#!/bin/bash

#SBATCH -J king
#SBATCH --mail-user=rczhang@u.northwestern.edu
#SBATCH --error=error.out
#SBATCH --output=output.out
#SBATCH --nodes=3
#SBATCH --ntasks-per-node=28
#SBATCH --mem=0
#SBATCH --time=120:00:00
#SBATCH --account=b1095
#SBATCH --partition=grail-std

module purge all
module load cmake/3.15.4
module load hdf5/1.10.7-openmpi-4.0.5-intel-19.0.5.281
module load mpi/openmpi-4.0.5-intel-19.0.5.281
module load gsl/2.5-intel-19.0.5.281
#########module load list

###mpirun -np X(=n_nodes*n_cores) <exe> > output
mpirun -np 84 ./cmc KingProfile.ini king

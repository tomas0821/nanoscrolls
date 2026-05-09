#!/bin/bash
#SBATCH --job-name=CNS_c3
#SBATCH --partition=parallel
#SBATCH --exclude=cn009
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=64
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --output=c3_32core.out
#SBATCH --error=c3_32core.err

# Load correct environment
module purge
module load ohpc
module swap gnu15 intel/2024.2.1
module load qe/7.5-cpu

# Create scratch dir
mkdir -p /scratch/global/tomas.rojas_s/ns/c3/out

echo "Starting c3 on 32 cores (out of 64 allocated)..."
cd c3

mpirun -np 32 pw.x -npool 2 -ntg 1 -in pw.in > pw.out 2>&1

echo "Finished c3"

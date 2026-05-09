#!/bin/bash
#SBATCH --job-name=CNS_c1_v73
#SBATCH --partition=parallel
#SBATCH --exclude=cn009
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=64
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --output=c1_v73.out
#SBATCH --error=c1_v73.err

# Load QE 7.3.1 environment
module purge
module load ohpc
module swap gnu15 intel/2024.2.1
module load qe/7.3.1-cpu

# Create scratch dir
SCRATCHDIR="/scratch/global/tomas.rojas_s/ns/c1/out"
mkdir -p "$SCRATCHDIR"

echo "Starting c1 on 64 cores using QE 7.3.1..."
cd c1

mpirun -np 64 pw.x -npool 1 -ntg 1 -in pw.in > pw.out 2>&1

echo "Finished c1"

#!/bin/bash
#SBATCH --job-name=CNS_pure_rst
#SBATCH --partition=parallel
#SBATCH --exclude=cn009
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=64
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --output=pure_cns_restart.out
#SBATCH --error=pure_cns_restart.err

module purge
module load ohpc
module swap gnu15 intel/2024.2.1
module load qe/7.5-cpu

SCRATCHDIR="/scratch/global/tomas.rojas_s/ns/pure_cns/out"
mkdir -p "$SCRATCHDIR"

echo "Starting pure_cns fresh from step-29 geometry..."
cd pure_cns

mpirun -np $SLURM_NTASKS pw.x -npool 1 -ntg 1 -in pw.in > pw.out 2>&1

echo "Finished pure_cns"

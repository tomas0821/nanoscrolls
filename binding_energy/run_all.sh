#!/bin/bash
#SBATCH --job-name=CNS_array
#SBATCH --partition=parallel
#SBATCH --exclude=cn009
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=64
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --output=array_%A_%a.out
#SBATCH --error=array_%A_%a.err
#SBATCH --array=1-3

# Load correct environment
module purge
module load ohpc
module swap gnu15 intel/2024.2.1
module load qe/7.5-cpu

case $SLURM_ARRAY_TASK_ID in
    1) CONFIG="c1" ;;
    2) CONFIG="c2" ;;
    3) CONFIG="c3" ;;
esac

SCRATCHDIR="/scratch/global/tomas.rojas_s/ns/${CONFIG}/out"
mkdir -p "$SCRATCHDIR"

echo "Starting calculation for $CONFIG on 1 node (64 cores)..."
cd $CONFIG

mpirun -np $SLURM_NTASKS pw.x -npool 1 -ntg 1 -in pw.in > pw.out 2>&1

echo "Finished $CONFIG"

#!/bin/bash
#SBATCH --job-name=CNS_refs
#SBATCH --partition=parallel
#SBATCH --exclude=cn009
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=64
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --output=ref_%A_%a.out
#SBATCH --error=ref_%A_%a.err
#SBATCH --array=1-2

# Load correct environment
module purge
module load ohpc
module swap gnu15 intel/2024.2.1
module load qe/7.4.1-cpu

if [ $SLURM_ARRAY_TASK_ID -eq 1 ]; then
    CONFIG="pure_cns"
    NPOOL=1
    NTG=2
elif [ $SLURM_ARRAY_TASK_ID -eq 2 ]; then
    CONFIG="alcl4_molecule"
    NPOOL=1
    NTG=1
fi

echo "Starting reference calculation for $CONFIG on 1 node (64 cores)..."
cd $CONFIG
rm -rf out && mkdir -p out

mpirun -np $SLURM_NTASKS pw.x -npool $NPOOL -ntg $NTG -in pw.in > pw.out 2>&1

echo "Finished $CONFIG"

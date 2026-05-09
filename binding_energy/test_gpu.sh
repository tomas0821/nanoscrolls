#!/bin/bash
#SBATCH --job-name=GPU_TEST_AlCl4
#SBATCH --partition=gpu
#SBATCH --exclude=cn009
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --time=00:30:00
#SBATCH --output=gpu_test_%j.out
#SBATCH --error=gpu_test_%j.err

# Load GPU module (v.7.5-gpu)
module purge
module load ohpc
module swap gnu15 intel/2024.2.1
module load qe/7.5-gpu

# Navigate to test folder - absolute path to be safe
cd /home/tomas.rojas_s/ns/binding_energy/alcl4_molecule

# Set scratch directory
SCRATCHDIR="./out_${SLURM_JOB_ID}"
mkdir -p "$SCRATCHDIR"

echo "Starting GPU test for AlCl4 on 1 GPU (Direct Call)..."
export OMP_NUM_THREADS=1

# Calling pw.x directly to avoid MPI binding issues on 1 rank
pw.x -in pw.in > pw_gpu_test_${SLURM_JOB_ID}.out 2>&1

echo "Finished GPU test"

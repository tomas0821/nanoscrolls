#!/bin/bash
#SBATCH --job-name=GPU_75_MCA
#SBATCH --partition=gpu
#SBATCH --exclude=cn009
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --time=00:30:00
#SBATCH --output=gpu_test_75_%j.out
#SBATCH --error=gpu_test_75_%j.err

# Clear environment
module purge
module load ohpc
module load qe/7.5-gpu

# Navigate to test folder
cd /home/tomas.rojas_s/ns/binding_energy/alcl4_molecule

# Set scratch directory
SCRATCHDIR="./out_gpu_75_${SLURM_JOB_ID}"
mkdir -p "$SCRATCHDIR"

echo "Starting GPU test for AlCl4 using QE 7.5-gpu (MCA Fix)..."
export OMP_NUM_THREADS=1

# Using absolute path and common flags for GPU QE to avoid binding issues
# --bind-to none and --mca btl_openib_allow_ib 1 to handle HPC quirks
mpirun -np 1 --bind-to none --mca btl_openib_allow_ib 1 /opt/ohpc/pub/apps/qe-7.5-gpu/bin/pw.x -in pw.in > pw_gpu_75_${SLURM_JOB_ID}.out 2>&1

echo "Finished GPU test with 7.5"

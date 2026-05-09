#!/bin/bash
#SBATCH --job-name=GPU_c1_V75
#SBATCH --partition=gpu
#SBATCH --exclude=cn009
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --time=24:00:00
#SBATCH --output=c1_gpu_%j.out
#SBATCH --error=c1_gpu_%j.err

# Load GPU module (v.7.5-gpu)
module purge
module load ohpc
module load qe/7.5-gpu

# Navigate to c1 folder
cd /home/tomas.rojas_s/ns/binding_energy/c1

# Set scratch directory
SCRATCHDIR="/scratch/global/tomas.rojas_s/ns/c1/out_gpu"
mkdir -p "$SCRATCHDIR"

echo "Starting c1 GPU run with 197 atoms using QE 7.5-gpu..."
export OMP_NUM_THREADS=1

# Use absolute path and flags that worked for the test
# Using np 1 since QE-GPU is most efficient with 1 rank per GPU for smaller atom counts
mpirun -np 1 --bind-to none --mca btl_openib_allow_ib 1 /opt/ohpc/pub/apps/qe-7.5-gpu/bin/pw.x -in pw.in > pw_gpu_c1_${SLURM_JOB_ID}.out 2>&1

echo "Finished c1 GPU run"

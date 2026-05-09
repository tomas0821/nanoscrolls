#!/bin/bash
#SBATCH --job-name=GPU_c1_2A100
#SBATCH --partition=gpu
#SBATCH --exclude=cn009
#SBATCH --nodes=1
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:2
#SBATCH --nodelist=cngpu001
#SBATCH --time=24:00:00
#SBATCH --output=c1_gpu_2_%j.out
#SBATCH --error=c1_gpu_2_%j.err

# Load modules
module purge
module load ohpc
module load qe/7.5-gpu

# Navigate to c1 folder
cd /home/tomas.rojas_s/ns/binding_energy/c1

# Set scratch directory
SCRATCHDIR="/scratch/global/tomas.rojas_s/ns/c1/out_gpu_2"
mkdir -p "$SCRATCHDIR"

echo "Starting c1 GPU run with 2 A100 GPUs on cngpu001..."
export OMP_NUM_THREADS=1

# Use 2 MPI ranks (1 per GPU)
mpirun -np 2 --bind-to none --mca btl_openib_allow_ib 1 pw.x -npool 1 -in pw.in > pw_gpu_c1_2_${SLURM_JOB_ID}.out 2>&1

echo "Finished c1 GPU run"

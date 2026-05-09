#!/bin/bash
#SBATCH --job-name=GPU_741_ABS
#SBATCH --partition=gpu
#SBATCH --exclude=cn009
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --time=00:30:00
#SBATCH --output=gpu_test_741_%j.out
#SBATCH --error=gpu_test_741_%j.err

# Clear environment
module purge
module load ohpc
# Manually set paths if module is being tricky
export PATH=/opt/ohpc/pub/apps/qe-7.4.1-gpu/bin:$PATH

# Navigate to test folder
cd /home/tomas.rojas_s/ns/binding_energy/alcl4_molecule

# Set scratch directory
SCRATCHDIR="./out_gpu_741_${SLURM_JOB_ID}"
mkdir -p "$SCRATCHDIR"

echo "Starting GPU test for AlCl4 using QE 7.4.1-gpu (Absolute Path)..."
export OMP_NUM_THREADS=1

# Calling pw.x using absolute path
/opt/ohpc/pub/apps/qe-7.4.1-gpu/bin/pw.x -in pw.in > pw_gpu_741_${SLURM_JOB_ID}.out 2>&1

echo "Finished GPU test with 7.4.1"

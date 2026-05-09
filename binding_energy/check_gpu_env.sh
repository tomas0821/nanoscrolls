#!/bin/bash
#SBATCH --job-name=CHECK_ENV
#SBATCH --partition=gpu
#SBATCH --exclude=cn009
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --time=00:10:00
#SBATCH --output=check_env_%j.out

module purge
module load ohpc
module load qe/7.5-gpu

echo "--- Module List ---"
module list

echo "--- Path ---"
echo $PATH

echo "--- LD_LIBRARY_PATH ---"
echo $LD_LIBRARY_PATH

echo "--- Which pw.x ---"
which pw.x

echo "--- LDD pw.x ---"
ldd $(which pw.x)

echo "--- Which mpirun ---"
which mpirun

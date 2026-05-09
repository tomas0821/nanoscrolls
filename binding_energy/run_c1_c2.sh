#!/bin/bash
#SBATCH --job-name=CNS_c1_c2
#SBATCH --partition=parallel
#SBATCH --exclude=cn009
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=64
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --output=c1_c2_shared.out
#SBATCH --error=c1_c2_shared.err

# Load correct environment
module purge
module load ohpc
module swap gnu15 intel/2024.2.1
module load qe/7.5-cpu

# Create scratch dirs
mkdir -p /scratch/global/tomas.rojas_s/ns/c1/out
mkdir -p /scratch/global/tomas.rojas_s/ns/c2/out

echo "Starting c1 and c2 concurrently (32 cores each)..."

# Run c1 in background
cd c1
mpirun -np 32 pw.x -npool 1 -ntg 1 -in pw.in > pw.out 2>&1 &
PID_C1=$!

# Run c2 in background
cd ../c2
mpirun -np 32 pw.x -npool 1 -ntg 1 -in pw.in > pw.out 2>&1 &
PID_C2=$!

echo "Jobs started with PIDs $PID_C1 and $PID_C2. Waiting for completion..."
wait $PID_C1 $PID_C2

echo "Finished c1 and c2"

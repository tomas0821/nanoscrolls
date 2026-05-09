# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Computational chemistry research project studying **carbon nanoscrolls (CNS) as cathode materials for aluminum-ion batteries (AIBs)**. The repository combines:
- DFT/MD simulations via Quantum ESPRESSO (run on HPC clusters via SLURM)
- Python scripts for parsing simulation outputs and generating visualizations
- A LaTeX research manuscript (APS/RevTeX4 format)

## Commands

### Manuscript Compilation (from `manuscript/`)
```bash
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```
Three pdflatex passes are required: first compiles, bibtex resolves references, second/third finalize cross-references.

### Data Processing (from project root)
```bash
python3 cns_comparison_final.py  # Generate comprehensive mixed energy/snapshot figures
python3 viz_all_extractions.py   # Generate large comparison panels for extraction studies
```

### Submitting SLURM Jobs (on HPC cluster)
```bash
cd binding_energy && sbatch run_c2_v73.sh
cd extraction_path && sbatch run_step.sh
cd axial_extraction && sbatch run_axial_step.sh
```

## QE Version & Stability Status

**Use `qe/7.3.1-cpu`**. This version has proven significantly more stable on the `parallel` partition than newer versions (7.4.x or 7.5.x).

### Current Stable Configuration
For all production systems (Main sites, Extractions, Normalization):
- **Cores:** 64 cores per job (`#SBATCH --ntasks-per-node=64`).
- **Parallel Flags:** `-npool 1 -ntg 1`.
- **Environment:**
  ```bash
  module purge
  module load ohpc
  module swap gnu15 intel/2024.2.1
  module load qe/7.3.1-cpu
  ```
- **Thresholds:**
    - Standard: `1.0D-4` Ry (Energy), `1.0D-3` Ry/Bohr (Force).
    - Config 2 (c2): `5.0D-3` Ry/Bohr (adjusted due to shallow potential well oscillation).

### Major Results (as of May 9, 2026)
- **Main Adsorption:** `c1` (-2.03 eV), `c2` (-1.86 eV), and `c3_diag` (-0.63 eV) are all converged.
- **Extraction Paths:** Both Radial and Axial paths have reached **Step 5** convergence. Step 6 is currently in progress.

## Resource Management

### GitHub Repository
- **Syncing:** `git pull origin main` before starting.
- **Committing:** `git add . && git commit -m "..." && git push origin main`.
- **Large Files:** Do not commit wavefunctions or scratch directories (see `.gitignore`).

### Scratch Policy
- **Directory Structure:** Always use `/scratch/global/tomas.rojas_s/ns/<study_name>/out`.
- **Disk Quota:** Regularly delete wavefunctions (`wfc*.dat`) in the `.save` directories of converged runs to prevent "Disk Quota Exceeded" errors. 
- **Restart Mode:** Use `restart_mode = 'restart'` for jobs nearing the 24h walltime limit.

## Architecture

### Data Flow
```
PACKMOL (structure prep)
       ↓
Quantum ESPRESSO pw.x  (DFT relaxation — 7.3.1 / 64 cores)
  binding_energy/c1, c2, c3     ← Adsorption site stability
  extraction_path/step_1...6    ← Radial extraction barrier
  axial_extraction/step_1...6   ← Longitudinal extraction barrier
       ↓
cns_comparison_final.py
  - Generates comprehensive mixed energy/snapshot figures.
  - Summarizes both studies (Radial vs. Axial) in a single publication plot.
```

### Key Conventions

**Energy units:** Quantum ESPRESSO outputs in Rydberg; `RY_TO_EV = 13.605693` used for conversion.

**SVG atomic colors:** C = gray (small), Al = red (large), Cl = green (medium)

**Coordinate systems:** `pw.in` uses angstroms (`ATOMIC_POSITIONS angstrom`).

**DFT parameters:** 45 Ry wavefunction cutoff, 360 Ry density cutoff, 1×1×3 k-points, DFT-D3 van der Waals, Marzari-Parinello smearing (degauss=0.02).

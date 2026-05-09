# Project Overview: Carbon Nanoscroll Cathode Study

This project contains a research manuscript titled **"Computational study of carbon nanoscrolls as cathodes in aluminum batteries"**. It explores the performance of Carbon Nanoscrolls (CNS) as a novel cathode material for Aluminum-ion batteries (AIBs) using Density Functional Theory (DFT) and Molecular Dynamics (MD) simulations.

The study investigates the adsorption of AlCl$_4^-$ anions within the nanoscroll galleries, analyzing electronic properties like Projected Density of States (PDOS) and structural behavior via Radial Distribution Functions (RDFs).

## Directory Structure and Key Files

- **`manuscript/`**: Main directory for the research paper.
    - **`main.tex`**: The primary LaTeX source file.
    - **`library.bib`**: BibTeX file containing all references.
    - **`fotos/`**: Directory containing figures and plots.
- **`binding_energy/`**: DFT relaxation studies for different adsorption configurations.
- **`extraction_path/`**: Radial extraction (de-intercalation) scan studies.
- **`axial_extraction/`**: Longitudinal extraction studies with vacuum gaps.

## Recent Simulation Results (May 9, 2026)

### Converged Configurations
Structural relaxations optimized with thresholds: $10^{-4}$ Ry (energy), $10^{-3}$ Ry/au (forces).
*Note: Config 2 used a $5 \times 10^{-3}$ Ry/au threshold to reach convergence.*
Reference $E_{pure} + E_{mol} = -3896.987915$ Ry.

| Configuration | Total Energy (Ry) | Binding Energy (eV) | Status |
| :--- | :--- | :--- | :--- |
| **Pristine CNS** | -3539.77765568 | - | Converged |
| **Config 1 (c1)** | -3897.13718526 | **-2.031 eV** | Converged |
| **Config 2 (c2)** | -3897.12477243 | **-1.862 eV** | Converged |
| **c3_rot90** | -3897.03401929 | **-0.627 eV** | Converged |
| **c3_diag** | -3897.03385204 | **-0.625 eV** | Converged |
| **c3_shift** | -3897.03274221 | **-0.610 eV** | Converged |
| **c3_flip** | -3897.03268854 | **-0.609 eV** | Converged |

### Sub-configuration Studies
- **c1 Study:** Confirmed `c1` as global minimum. Perturbations (`rot90`, `flip`) increased energy by +0.5 to +1.0 eV. `c1_shift` migrated back to the original `c1` site.
- **c3 Study:** Completed. All four orientations converged. **`c3_rot90`** and **`c3_diag`** found the most stable orientations (~ -0.627 eV), confirming the diagonal/orthogonal alignment as the physical preference for this gallery site.

### Extraction Path Study (Relaxed Scans)
Determining the energy barriers for $AlCl_4^-$ de-intercalation.

1.  **Radial Path (Gallery Exit):**
    *   **Steps 1-4:** Smooth descent from -3897.1336 to -3897.1630 Ry.
    *   **Step 5:** Slight energy increase to -3897.1581 Ry (+0.06 eV), marking the exit onset.
    *   **Step 6:** Running (Current force: 0.0027 Ry/au).

2.  **Axial Path (Longitudinal Exit):**
    *   **Step 1 (Mouth):** -3886.3163 Ry.
    *   **Step 2 (Bulk Min):** -3886.5476 Ry (Global minimum of the axial segment).
    *   **Steps 3-5:** Energy climbing from -3886.5445 to -3886.5300 Ry.
    *   **Barrier:** Current barrier of **+0.24 eV** relative to the axial minimum (Step 2).
    *   **Step 6:** Running.

## GitHub Repository Management

This project is hosted on GitHub for version control and collaboration.

### 1. Initial Setup (on a new machine)
If the repository is not yet cloned:
```bash
git clone https://github.com/USERNAME/ns.git
cd ns
```

### 2. Common Workflow
Always pull before starting work to ensure you have the latest results:
```bash
git pull origin main
```

To commit and push your changes (plots, documentation, or scripts):
```bash
git add .
git commit -m "Describe your changes (e.g., updated Step 5 results)"
git push origin main
```

### 3. Managing Large Files
**Important:** Do NOT commit large simulation output files, wavefunctions, or scratch directories. The following are automatically ignored via `.gitignore`:
- `*.save/` (QE scratch directories)
- `out/` (Local output folders)
- `*.err`, `*.out` (Slurm logs and raw QE outputs, unless specifically needed)
- `gh.tar.gz`, `gh_cli/` (Binary distributions)

### 4. GitHub CLI (Optional)
The GitHub CLI (`gh`) is available in the `gh_cli/bin/` directory for managing pull requests and issues directly from the terminal:
```bash
./gh_cli/bin/gh auth status
./gh_cli/bin/gh repo view
```

### 5. Agent-Led Repository Management
If you are instructing another agent to manage this repository, provide them with these guidelines:

**Authentication:**
- **SSH (Preferred):** Ensure the agent's environment has a valid SSH key added to GitHub.
- **PAT (Token):** Alternatively, use a Personal Access Token for HTTPS authentication.

**Mandatory Workflow for Agents:**
1.  **Credential Access:** Look for a `GITHUB_TOKEN` in the environment variables or a local (git-ignored) `.env` file. Check `~/.ssh/` for existing keys.
2.  **Status Check:** Run `git status` and `git remote -v` to verify the environment.
2.  **Pull First:** Always run `git pull origin main` before making any modifications.
3.  **Surgical Commits:** Only commit small files (scripts, `.md` files, plots). 
4.  **Verification:** Before pushing, verify that NO large simulation files are staged (check `git status`).
5.  **Push:** Use `git push origin main`.

**Standard Instruction for New Agents:**
> "You are an agent managing a DFT research repository. Your task is to keep the GitHub remote synchronized. Always pull before starting. Never commit folders ending in `.save/`, `out/`, or files over 50MB. Focus your commits on documentation (`GEMINI.md`, `CLAUDE.md`), analysis scripts (`*.py`), and generated figures (`*.png`, `*.svg`)."

## Methodology Updates
- **Thresholds:** Using $10^{-4}$ Ry / $10^{-3}$ Ry/au for all production relaxations.
- **Anchoring:** Axial extraction uses a fixed bottom layer of Carbon atoms to simulate bulk scroll stability.
- **Parameters:** Consistent 45 Ry cutoff, 1x1x3 k-points (1x1x1 for large axial cell), and `dft-d3` vdW correction.

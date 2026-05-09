import os
import re

def extract_from_file(filepath, header_pattern):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    idx = -1
    for i, line in enumerate(lines):
        if header_pattern in line:
            idx = i
    
    if idx == -1:
        return None
    
    result_lines = []
    if "ATOMIC_POSITIONS" in header_pattern:
        for line in lines[idx+1:]:
            if "End final" in line or "writing" in line or any(h in line for h in ["K_POINTS", "CELL_PARAMETERS"]):
                break
            if line.strip() != "":
                result_lines.append(line.strip())
        return "\n".join(result_lines)
    
    if "CELL_PARAMETERS" in header_pattern:
        cell_lines = lines[idx:idx+4]
        return "".join(cell_lines).strip()
    
    if "ATOMIC_SPECIES" in header_pattern:
        for line in lines[idx:]:
            if "K_POINTS" in line:
                break
            if line.strip() != "":
                result_lines.append(line.strip())
        return "\n".join(result_lines)
    
    return None

def create_input(name, outfile, original_in):
    pos = extract_from_file(outfile, "ATOMIC_POSITIONS (angstrom)")
    cell = extract_from_file(outfile, "CELL_PARAMETERS (angstrom)")
    if not pos: pos = extract_from_file(original_in, "ATOMIC_POSITIONS")
    if not cell: cell = extract_from_file(original_in, "CELL_PARAMETERS")
    species = extract_from_file(original_in, "ATOMIC_SPECIES")

    if not pos:
        print(f"Failed to extract positions for {name}")
        return

    with open(original_in, 'r') as f:
        orig_content = f.read()
    
    nat = re.search(r"nat\s*=\s*(\d+)", orig_content).group(1)
    ntyp = re.search(r"ntyp\s*=\s*(\d+)", orig_content).group(1)

    template = f"""&CONTROL
    calculation = 'relax'
    restart_mode = 'from_scratch'
    prefix = 'ns'
    outdir = '/scratch/global/tomas.rojas_s/ns/normalization_lateral/{name}/out'
    pseudo_dir = '/home/tomas.rojas_s/pseudo/'
    forc_conv_thr = 1.0D-3
    etot_conv_thr = 1.0D-4
    nstep = 200
/
&SYSTEM
    ibrav = 0
    nat = {nat}
    ntyp = {ntyp}
    ecutwfc = 45.0
    occupations = 'smearing'
    smearing = 'mp'
    degauss = 0.02
    vdw_corr = 'dft-d3'
/
&ELECTRONS
    mixing_beta = 0.7
    conv_thr = 1.0D-6
/
&IONS
    ion_dynamics = 'bfgs'
/
&CELL
/

{species}

K_POINTS automatic
1 1 3 0 0 0

{cell if cell else ""}

ATOMIC_POSITIONS (angstrom)
{pos}
"""
    os.makedirs(f"normalization_lateral/{name}", exist_ok=True)
    with open(f"normalization_lateral/{name}/pw.in", 'w') as f:
        f.write(template)
    print(f"Created normalization_lateral/{name}/pw.in")

# Detect all sites
sites_dir = "Lateral_adsorption"
for d in sorted(os.listdir(sites_dir)):
    dir_path = os.path.join(sites_dir, d)
    if not os.path.isdir(dir_path): continue
    
    # Identify type and site number
    match = re.search(r"(\d+)(alcl3|et)", d)
    if not match: continue
    num, series = match.groups()
    name = f"{series}_site{num}"
    
    # Identify input and output files
    # For alcl3, input is num.in (e.g. 1.in), output is num.out
    # For et, input is numet.in (e.g. 1et.in), output is numet.out
    if series == "alcl3":
        ini = os.path.join(dir_path, f"{num}.in")
        out = os.path.join(dir_path, f"{num}.out")
    else:
        ini = os.path.join(dir_path, f"{num}et.in")
        out = os.path.join(dir_path, f"{num}et.out")
        
    create_input(name, out, ini)

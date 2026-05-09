import os
import re

def extract_block(infile, start_tag):
    if not os.path.exists(infile):
        return None
    with open(infile, 'r') as f:
        lines = f.readlines()
    
    idx = -1
    for i, line in enumerate(lines):
        if start_tag in line:
            idx = i
            break
            
    if idx == -1: return None
    
    res = [lines[idx].strip()]
    for line in lines[idx+1:]:
        if line.strip() == "" or any(h in line for h in ["K_POINTS", "ATOMIC_POSITIONS", "CELL_PARAMETERS", "End final"]):
            break
        res.append(line.strip())
    return "\n".join(res)

def create_pristine(name, source_in, species_to_keep):
    # Extract Cell
    cell = extract_block(source_in, "CELL_PARAMETERS")
    
    # Extract Pos
    pos_block = extract_block(source_in, "ATOMIC_POSITIONS")
    if not pos_block:
        print(f"Failed to extract positions from {source_in}")
        return
        
    pos_lines = pos_block.split('\n')[1:]
    filtered_pos = [l for l in pos_lines if l.split()[0] in species_to_keep]
    nat = len(filtered_pos)
    pos_str = "\n".join(filtered_pos)
    
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
    ntyp = 1
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

ATOMIC_SPECIES
C 12.011 C.pbe-n-kjpaw_psl.1.0.0.UPF

K_POINTS automatic
1 1 3 0 0 0

{cell}

ATOMIC_POSITIONS (angstrom)
{pos_str}
"""
    os.makedirs(f"normalization_lateral/{name}", exist_ok=True)
    with open(f"normalization_lateral/{name}/pw.in", 'w') as f:
        f.write(template)
    print(f"Created {name}/pw.in with {nat} C atoms")

create_pristine("pure_scroll_193", "normalization_lateral/alcl3_site7/pw.in", ["C"])
create_pristine("pure_scroll_199", "normalization_lateral/et_site5/pw.in", ["C"])

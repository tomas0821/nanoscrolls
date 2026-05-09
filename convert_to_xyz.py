import os
import re

def extract_xyz(outfile):
    with open(outfile, 'r') as f:
        lines = f.readlines()
    
    # Find last ATOMIC_POSITIONS (angstrom)
    pos_idx = -1
    for i, line in enumerate(lines):
        if "ATOMIC_POSITIONS (angstrom)" in line:
            pos_idx = i
            
    if pos_idx == -1:
        # Try without parenthesis
        for i, line in enumerate(lines):
            if "ATOMIC_POSITIONS angstrom" in line:
                pos_idx = i
    
    if pos_idx == -1:
        return None
    
    atoms = []
    for line in lines[pos_idx+1:]:
        if line.strip() == "" or any(h in line for h in ["End final", "writing", "K_POINTS", "CELL_PARAMETERS"]):
            break
        if len(line.split()) >= 4:
            atoms.append(line.strip())
            
    return atoms

output_dir = "Lateral_adsorption_xyz"
os.makedirs(output_dir, exist_ok=True)

source_dir = "Lateral_adsorption"
for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.endswith(".out"):
            filepath = os.path.join(root, file)
            atoms = extract_xyz(filepath)
            
            if atoms:
                # Create a name based on the directory
                parent = os.path.basename(root)
                xyz_name = f"{parent}.xyz"
                xyz_path = os.path.join(output_dir, xyz_name)
                
                with open(xyz_path, 'w') as f:
                    f.write(f"{len(atoms)}\n")
                    f.write(f"Converted from {filepath}\n")
                    for atom in atoms:
                        f.write(f"{atom}\n")
                print(f"Converted {filepath} -> {xyz_path}")
            else:
                print(f"Failed to find positions in {filepath}")

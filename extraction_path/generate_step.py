import os
import re
import sys

def parse_atoms_from_out(filepath):
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return []
    with open(filepath, 'r') as f:
        content = f.read()
    matches = list(re.finditer(r"ATOMIC_POSITIONS\s+\(([^)]+)\)", content))
    if not matches: 
        print(f"Error: No ATOMIC_POSITIONS found in {filepath}.")
        return []
    match = matches[-1]
    unit = match.group(1).lower()
    start_idx = match.end()
    atoms = []
    lines = content[start_idx:].strip().split('\n')
    for line in lines:
        parts = line.split()
        if len(parts) < 4: break
        if parts[0] in ['C', 'Al', 'Cl']:
            atoms.append([parts[0], float(parts[1]), float(parts[2]), float(parts[3])])
    return atoms

def generate_next_radial_step(prev_step, next_step, shift_x=1.0, shift_y=-0.5):
    # 1. Load relaxed coords from previous step
    prev_out = f'step_{prev_step}/pw.out'
    atoms = parse_atoms_from_out(prev_out)
    if not atoms: return
    
    # 2. Apply shift to molecule (last 5 atoms)
    mol_start_idx = 192
    new_atoms = []
    for i, (s, x, y, z) in enumerate(atoms):
        if i >= mol_start_idx:
            new_atoms.append([s, x + shift_x, y + shift_y, z, 0 if s == 'Al' else 1])
        else:
            new_atoms.append([s, x, y, z, 1])
            
    # 3. Read template header from previous input
    with open(f'step_{prev_step}/pw.in', 'r') as f:
        template = f.read()
    
    header = template.split('ATOMIC_POSITIONS')[0]
    header = header.replace(f'step_{prev_step}/out', f'step_{next_step}/out')
    header = header.replace("restart_mode = 'restart'", "restart_mode = 'from_scratch'")
    
    # 4. Write new input
    os.makedirs(f'step_{next_step}', exist_ok=True)
    with open(f'step_{next_step}/pw.in', 'w') as f:
        f.write(header)
        f.write("ATOMIC_POSITIONS angstrom\n")
        for s, x, y, z, free in new_atoms:
            fix_str = "0 0 0" if free == 0 else "1 1 1"
            f.write(f"{s:<12} {x:18.10f} {y:18.10f} {z:18.10f} {fix_str}\n")
    print(f"Successfully generated step_{next_step}/pw.in from step_{prev_step}/pw.out.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 generate_step.py <prev_step> <next_step> [shift_x] [shift_y]")
    else:
        p_step = int(sys.argv[1])
        n_step = int(sys.argv[2])
        sx = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        sy = float(sys.argv[4]) if len(sys.argv) > 4 else -0.5
        generate_next_radial_step(p_step, n_step, sx, sy)

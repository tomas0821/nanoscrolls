import os
import math

def rotate_point(x, y, z, cx, cy, cz, angle_deg, axis='z'):
    angle = math.radians(angle_deg)
    # Translate to origin
    nx, ny, nz = x - cx, y - cy, z - cz
    if axis == 'z':
        rx = nx * math.cos(angle) - ny * math.sin(angle)
        ry = nx * math.sin(angle) + ny * math.cos(angle)
        rz = nz
    elif axis == 'x':
        rx = nx
        ry = ny * math.cos(angle) - nz * math.sin(angle)
        rz = ny * math.sin(angle) + nz * math.cos(angle)
    # Translate back
    return rx + cx, ry + cy, rz + cz

def generate_subconfig(name, rotation_angle=0, rotation_axis='z', shift_x=0):
    with open('c1_converged.txt', 'r') as f:
        lines = f.readlines()[1:] # skip header
    
    atoms = []
    for line in lines:
        parts = line.split()
        if len(parts) < 4: continue
        atoms.append([parts[0], float(parts[1]), float(parts[2]), float(parts[3])])
    
    # Molecule is atoms index 192 to 196 (last 5)
    mol_atoms = atoms[192:]
    scroll_atoms = atoms[:192]
    
    # Al center
    cx, cy, cz = mol_atoms[0][1], mol_atoms[0][2], mol_atoms[0][3]
    
    new_mol = []
    for s, x, y, z in mol_atoms:
        # Apply rotation
        nx, ny, nz = rotate_point(x, y, z, cx, cy, cz, rotation_angle, rotation_axis)
        # Apply shift
        nx += shift_x
        new_mol.append([s, nx, ny, nz])
    
    new_atoms = scroll_atoms + new_mol
    
    # Create directory
    os.makedirs(name, exist_ok=True)
    
    # Write pw.in
    # Get template from c1
    with open('c1/pw.in', 'r') as f:
        template = f.read()
    
    # Update thresholds and scratch dir
    header = template.split('ATOMIC_POSITIONS')[0]
    header = header.replace('c1/out', f'{name}/out')
    header = header.replace("restart_mode = 'restart'", "restart_mode = 'from_scratch'")
    header = header.replace("etot_conv_thr = 1.0D-5", "etot_conv_thr = 1.0D-4")
    header = header.replace("forc_conv_thr = 1.0D-4", "forc_conv_thr = 1.0D-3")
    
    with open(f'{name}/pw.in', 'w') as f:
        f.write(header)
        f.write("ATOMIC_POSITIONS angstrom\n")
        for s, x, y, z in new_atoms:
            f.write(f"{s:<12} {x:18.10f} {y:18.10f} {z:18.10f}\n")

# Generate the 4 proposed variants
generate_subconfig('c1_rot90', rotation_angle=90, rotation_axis='z')
generate_subconfig('c1_flip', rotation_angle=180, rotation_axis='x')
generate_subconfig('c1_shift', shift_x=1.42)
generate_subconfig('c1_diag', rotation_angle=45, rotation_axis='z')

print("Generated directories and pw.in for: c1_rot90, c1_flip, c1_shift, c1_diag")

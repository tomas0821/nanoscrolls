import os
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def parse_atoms(filepath):
    if not os.path.exists(filepath): return []
    with open(filepath, 'r') as f:
        content = f.read()
    matches = list(re.finditer(r"ATOMIC_POSITIONS\s+\(?([^)\n]+)\)?", content))
    if not matches: return []
    match = matches[-1]
    unit = match.group(1).lower()
    start_idx = match.end()
    atoms = []
    lines = content[start_idx:].strip().split('\n')
    for line in lines:
        parts = line.split()
        if len(parts) < 4: break
        if parts[0] in ['C', 'Al', 'Cl']:
            scale = 50.0 if "alat" in unit else 1.0
            atoms.append({'s': parts[0], 'x': float(parts[1])*scale, 'y': float(parts[2])*scale, 'z': float(parts[3])*scale})
    return atoms

def detect_bonds(atoms):
    bonds = []
    cc_range = (1.0**2, 1.7**2); alcl_range = (1.5**2, 2.6**2)
    n = len(atoms)
    for i in range(n):
        for j in range(i + 1, n):
            dx, dy, dz = atoms[i]['x'] - atoms[j]['x'], atoms[i]['y'] - atoms[j]['y'], atoms[i]['z'] - atoms[j]['z']
            d2 = dx*dx + dy*dy + dz*dz
            s_pair = {atoms[i]['s'], atoms[j]['s']}
            if s_pair == {'C'} and cc_range[0] < d2 < cc_range[1]: bonds.append((i, j, '#888'))
            elif s_pair == {'Al', 'Cl'} and alcl_range[0] < d2 < alcl_range[1]: bonds.append((i, j, '#333'))
    return bonds

def plot_view(ax, atoms, bonds, view='yz', title=""):
    props = {'C': {'color': '#444444', 'radius': 0.40, 'zorder': 10},
             'Al': {'color': '#e74c3c', 'radius': 0.80, 'zorder': 30},
             'Cl': {'color': '#27ae60', 'radius': 0.65, 'zorder': 20}}
    v_map = {'yz': ('y', 'z', 'x'), 'xz': ('x', 'z', 'y'), 'xy': ('x', 'y', 'z')}
    vx, vy, vz = v_map[view]
    for i, j, color in bonds:
        ax.plot([atoms[i][vx], atoms[j][vx]], [atoms[i][vy], atoms[j][vy]], color=color, lw=1.0, solid_capstyle='round', zorder=5, alpha=0.3)
    sorted_atoms = sorted(atoms, key=lambda a: a[vz])
    for a in sorted_atoms:
        p = props[a['s']]
        ax.add_patch(Circle((a[vx], a[vy]), p['radius'], color=p['color'], ec='black', lw=0.2, alpha=0.9, zorder=p['zorder']))
    ax.set_aspect('equal'); ax.set_title(title, fontsize=10, fontweight='bold'); ax.axis('off')
    all_vx, all_vy = [a[vx] for a in atoms], [a[vy] for a in atoms]
    ax.set_xlim(min(all_vx)-2, max(all_vx)+2); ax.set_ylim(min(all_vy)-2, max(all_vy)+2)

def generate_full_comparison():
    configs = [
        ('extraction_path/step_1/pw.out', 'Radial Step 1 (Relaxed)'),
        ('extraction_path/step_2/pw.out', 'Radial Step 2 (Relaxing)'),
        ('axial_extraction/step_1/pw.out', 'Axial Step 1 (Relaxed)'),
        ('axial_extraction/step_2/pw.out', 'Axial Step 2 (Relaxed)'),
        ('axial_extraction/step_3/pw.in',  'Axial Step 3 (Setup)')
    ]
    
    fig, axes = plt.subplots(5, 3, figsize=(18, 28), dpi=200)
    
    for row, (path, label) in enumerate(configs):
        atoms = parse_atoms(path)
        if not atoms: continue
        bonds = detect_bonds(atoms)
        
        plot_view(axes[row, 0], atoms, bonds, view='xy', title=f"{label}\nCross-section (XY)")
        plot_view(axes[row, 1], atoms, bonds, view='yz', title=f"Side View (YZ)")
        plot_view(axes[row, 2], atoms, bonds, view='xz', title=f"Top View (XZ)")
        
        if row >= 2: # Axial cases
            for col in [1, 2]:
                axes[row, col].axhline(y=16.2, color='red', linestyle='--', lw=1.2)
                axes[row, col].axhline(y=8.8, color='red', linestyle='--', lw=1.2)

    plt.tight_layout()
    plt.savefig('all_extractions_comparison.png', bbox_inches='tight')
    print("Generated: all_extractions_comparison.png (5 stages)")

if __name__ == "__main__":
    generate_full_comparison()

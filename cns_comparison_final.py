import os
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.gridspec as gridspec

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

def plot_structure(ax, atoms, bonds, view='yz', title=""):
    props = {'C': {'color': '#444444', 'radius': 0.35, 'zorder': 10},
             'Al': {'color': '#e74c3c', 'radius': 0.70, 'zorder': 30},
             'Cl': {'color': '#27ae60', 'radius': 0.55, 'zorder': 20}}
    v_map = {'yz': ('y', 'z', 'x'), 'xz': ('x', 'z', 'y'), 'xy': ('x', 'y', 'z')}
    vx, vy, vz = v_map[view]
    for i, j, color in bonds:
        ax.plot([atoms[i][vx], atoms[j][vx]], [atoms[i][vy], atoms[j][vy]], color=color, lw=0.8, solid_capstyle='round', zorder=5, alpha=0.15)
    sorted_atoms = sorted(atoms, key=lambda a: a[vz])
    for a in sorted_atoms:
        p = props[a['s']]
        ax.add_patch(Circle((a[vx], a[vy]), p['radius'], color=p['color'], ec='black', lw=0.1, alpha=0.9, zorder=p['zorder']))
    ax.set_aspect('equal'); ax.set_title(title, fontsize=8, fontweight='bold'); ax.axis('off')
    all_vx, all_vy = [a[vx] for a in atoms], [a[vy] for a in atoms]
    if not all_vx: return
    ax.set_xlim(min(all_vx)-1, max(all_vx)+1); ax.set_ylim(min(all_vy)-1, max(all_vy)+1)

# DATA
axial_z = [11.22, 12.22, 13.22, 14.22]
axial_e = [-3886.31630129, -3886.54756335, -3886.54448333, -3886.53867251]
axial_rel = [(e - min(axial_e)) * 13.605693 for e in axial_e]

radial_dist = [0.0, 1.0, 2.0, 3.0, 4.0]
radial_e = [-3897.13358894, -3897.14873251, -3897.15100181, -3897.16298017, -3897.15810703]
radial_rel = [(e - min(radial_e)) * 13.605693 for e in radial_e]

fig = plt.figure(figsize=(26, 10), dpi=200)
gs = gridspec.GridSpec(2, 7, width_ratios=[1.8, 1, 1, 1, 1, 1, 1])

# --- ROW 0: RADIAL ---
ax_rad_e = fig.add_subplot(gs[0, 0])
ax_rad_e.plot(radial_dist, radial_rel, 'o-', color='#3498db', lw=2, markersize=8)
ax_rad_e.set_title("Radial Extraction Energy", fontweight='bold')
ax_rad_e.set_ylabel("Relative Energy (eV)")
ax_rad_e.set_xlabel("Displacement ($\AA$)")
ax_rad_e.grid(True, alpha=0.3)

radial_steps = [
    ('extraction_path/step_1/pw.out', 'Step 1 (Rel)'),
    ('extraction_path/step_2/pw.out', 'Step 2 (Rel)'),
    ('extraction_path/step_3/pw.out', 'Step 3 (Rel)'),
    ('extraction_path/step_4/pw.out', 'Step 4 (Rel)'),
    ('extraction_path/step_5/pw.out', 'Step 5 (Rel)'),
    ('extraction_path/step_6/pw.in',  'Step 6 (Setup)')
]

for i, (path, label) in enumerate(radial_steps):
    ax = fig.add_subplot(gs[0, i+1])
    atoms = parse_atoms(path)
    if atoms: plot_structure(ax, atoms, detect_bonds(atoms), view='xy', title=f"Radial {label}")

# --- ROW 1: AXIAL ---
ax_ax_e = fig.add_subplot(gs[1, 0])
ax_ax_e.plot(axial_z, axial_rel, 'o-', color='#e67e22', lw=2, markersize=8)
ax_ax_e.set_title("Axial Extraction Energy", fontweight='bold')
ax_ax_e.set_ylabel("Relative Energy (eV)")
ax_ax_e.set_xlabel("Al position Z ($\AA$)")
ax_ax_e.grid(True, alpha=0.3)
ax_ax_e.axvspan(8.8, 14.87, color='gray', alpha=0.1)

axial_steps = [
    ('axial_extraction/step_1/pw.out', 'Step 1 (Rel)'),
    ('axial_extraction/step_2/pw.out', 'Step 2 (Rel)'),
    ('axial_extraction/step_3/pw.out', 'Step 3 (Rel)'),
    ('axial_extraction/step_4/pw.out', 'Step 4 (Rel)'),
    ('axial_extraction/step_5/pw.in',  'Step 5 (Setup)')
]

for i, (path, label) in enumerate(axial_steps):
    ax = fig.add_subplot(gs[1, i+1])
    atoms = parse_atoms(path)
    if atoms: plot_structure(ax, atoms, detect_bonds(atoms), view='yz', title=f"Axial {label}")

plt.tight_layout()
plt.savefig('cns_comparison_final.png')
print("Generated updated cns_comparison_final.png (Radial Step 5 included)")

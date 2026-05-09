import os
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D

def parse_atoms(filepath, from_in_file=False):
    if not os.path.exists(filepath): return []
    with open(filepath, 'r') as f:
        content = f.read()
    if from_in_file:
        matches = list(re.finditer(r"ATOMIC_POSITIONS\s+\(?([^\)\n]+)\)?", content))
    else:
        matches = list(re.finditer(r"ATOMIC_POSITIONS\s+\(([^)]+)\)", content))
    if not matches: return []
    match = matches[0] if from_in_file else matches[-1]
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

def detect_bonds(atoms, zoom_center=None, zoom_range=None):
    bonds = []
    # Distance thresholds squared
    cc_range = (1.0**2, 1.7**2)
    alcl_range = (1.5**2, 2.6**2)
    
    n = len(atoms)
    for i in range(n):
        # If zooming, only check atoms near center to save time
        if zoom_center and zoom_range:
            dist_to_zoom = (atoms[i]['x']-zoom_center['x'])**2 + (atoms[i]['y']-zoom_center['y'])**2
            if dist_to_zoom > (zoom_range*1.5)**2: continue
            
        for j in range(i + 1, n):
            dx = atoms[i]['x'] - atoms[j]['x']
            dy = atoms[i]['y'] - atoms[j]['y']
            dz = atoms[i]['z'] - atoms[j]['z']
            d2 = dx*dx + dy*dy + dz*dz
            
            s_pair = {atoms[i]['s'], atoms[j]['s']}
            if s_pair == {'C'} and cc_range[0] < d2 < cc_range[1]:
                bonds.append((i, j, '#888'))
            elif s_pair == {'Al', 'Cl'} and alcl_range[0] < d2 < alcl_range[1]:
                bonds.append((i, j, '#333'))
    return bonds

def plot_atom_view(ax, atoms, view='xy', zoom=None, title=""):
    if not atoms:
        ax.axis('off')
        return

    props = {
        'C':  {'color': '#444444', 'radius': 0.45, 'zorder': 10},
        'Al': {'color': '#e74c3c', 'radius': 0.80, 'zorder': 30},
        'Cl': {'color': '#27ae60', 'radius': 0.65, 'zorder': 20}
    }
    
    al_atom = next((a for a in atoms if a['s'] == 'Al'), None)
    v_map = {'xy': ('x', 'y', 'z'), 'xz': ('x', 'z', 'y')}
    vx, vy, vz = v_map[view]
    
    if zoom and al_atom:
        ref_x, ref_y, limit = al_atom[vx], al_atom[vy], zoom
        bonds = detect_bonds(atoms, zoom_center=al_atom, zoom_range=zoom)
    else:
        if view == 'xy': ref_x, ref_y, limit = 25.0, 30.0, 12.0
        else: ref_x, ref_y, limit = 25.0, 3.5, 15.0
        bonds = detect_bonds(atoms)

    # 1. Draw Sticks (Bonds)
    for i, j, color in bonds:
        ax.plot([atoms[i][vx], atoms[j][vx]], [atoms[i][vy], atoms[j][vy]], 
                color=color, lw=1.5, solid_capstyle='round', zorder=5, alpha=0.6)

    # 2. Draw Balls (Atoms)
    sorted_atoms = sorted(atoms, key=lambda a: a[vz])
    for a in sorted_atoms:
        # Visibility check for performance and zoom
        if abs(a[vx]-ref_x) > limit+1 or abs(a[vy]-ref_y) > limit+1: continue
        
        p = props[a['s']]
        main_circ = Circle((a[vx], a[vy]), p['radius'], color=p['color'], ec='black', lw=0.5, alpha=0.95, zorder=p['zorder'])
        ax.add_patch(main_circ)
        highlight = Circle((a[vx] - p['radius']*0.3, a[vy] + p['radius']*0.3), p['radius']*0.2, color='white', alpha=0.4, zorder=p['zorder']+1)
        ax.add_patch(highlight)

    ax.set_aspect('equal')
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.axis('off')
    ax.set_xlim(ref_x - limit, ref_x + limit)
    ax.set_ylim(ref_y - limit, ref_y + limit)

def generate_ball_and_stick():
    configs = [('c1', 'Original c1'), ('c1_rot90', 'c1 Rotated 90'), ('c1_flip', 'c1 Inverted'), 
               ('c1_shift', 'c1 Shifted 1.4A'), ('c1_diag', 'c1 Diagonal 45')]
    
    fig, axes = plt.subplots(len(configs), 3, figsize=(18, 5 * len(configs)), dpi=200)
    for i, (folder, name) in enumerate(configs):
        init_atoms = parse_atoms(f'{folder}/pw.in', from_in_file=True)
        final_atoms = parse_atoms(f'{folder}/pw.out', from_in_file=False)
        plot_atom_view(axes[i, 0], init_atoms, view='xz', zoom=5.0, title=f"{name}\nInitial")
        plot_atom_view(axes[i, 1], final_atoms, view='xz', zoom=5.0, title="Relaxed Detail")
        plot_atom_view(axes[i, 2], final_atoms, view='xy', title="Overall Relaxed")

    plt.tight_layout()
    plt.savefig('c1_ball_and_stick_study.png', bbox_inches='tight')
    print("Generated: c1_ball_and_stick_study.png")

generate_ball_and_stick()

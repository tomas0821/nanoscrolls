import os
import re
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def parse_atoms(filepath):
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
        if parts[0] in ['C', 'Al', 'Cl', 'H', 'N']:
            scale = 1.0 # Assuming angstrom
            atoms.append({'s': parts[0], 'x': float(parts[1])*scale, 'y': float(parts[2])*scale, 'z': float(parts[3])*scale})
    return atoms

def plot_lateral(filepath, output_name):
    atoms = parse_atoms(filepath)
    if not atoms: return
    
    fig, ax = plt.subplots(figsize=(8, 8))
    props = {'C': {'color': '#444444', 'radius': 0.3, 'zorder': 1},
             'Al': {'color': '#e74c3c', 'radius': 0.6, 'zorder': 5},
             'Cl': {'color': '#27ae60', 'radius': 0.5, 'zorder': 4},
             'H': {'color': '#bdc3c7', 'radius': 0.2, 'zorder': 2},
             'N': {'color': '#3498db', 'radius': 0.4, 'zorder': 3}}
    
    for a in atoms:
        p = props.get(a['s'], {'color': 'gray', 'radius': 0.3, 'zorder': 0})
        ax.add_patch(Circle((a['x'], a['y']), p['radius'], color=p['color'], ec='black', lw=0.1, zorder=p['zorder']))
    
    ax.set_aspect('equal')
    xs = [a['x'] for a in atoms]
    ys = [a['y'] for a in atoms]
    ax.set_xlim(min(xs)-2, max(xs)+2)
    ax.set_ylim(min(ys)-2, max(ys)+2)
    ax.set_title(f"Lateral Adsorption: {os.path.basename(filepath)}")
    plt.savefig(output_name)
    print(f"Saved {output_name}")

# Plot a few to compare
plot_lateral('Lateral_adsorption/1alcl3/1.in', 'lateral_1alcl3.png')
plot_lateral('Lateral_adsorption/7alcl3/7.in', 'lateral_7alcl3.png')
plot_lateral('Lateral_adsorption/1et/1et.in', 'lateral_1et.png')
plot_lateral('Lateral_adsorption/5et/5et.in', 'lateral_5et.png')

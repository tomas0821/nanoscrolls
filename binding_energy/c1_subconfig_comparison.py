import os
import re

def parse_atoms(filepath, find_first=True, from_in_file=False):
    if not os.path.exists(filepath): return []
    with open(filepath, 'r') as f:
        content = f.read()
    
    if from_in_file:
        matches = list(re.finditer(r"ATOMIC_POSITIONS\s+\(?([^\)\n]+)\)?", content))
    else:
        matches = list(re.finditer(r"ATOMIC_POSITIONS\s+\(([^)]+)\)", content))
    
    if not matches: return []
    
    match = matches[0] if find_first else matches[-1]
    unit = match.group(1).lower()
    start_idx = match.end()
    
    atoms = []
    lines = content[start_idx:].strip().split('\n')
    for line in lines:
        parts = line.split()
        if len(parts) < 4: break
        if parts[0] in ['C', 'Al', 'Cl']:
            try:
                scale = 50.0 if "alat" in unit else 1.0
                atoms.append({'s': parts[0], 'x': float(parts[1])*scale, 'y': float(parts[2])*scale, 'z': float(parts[3])*scale})
            except: break
    return atoms

def get_svg_view(atoms, title, x_off, y_off, view='xy', zoom=None, scale=15):
    if not atoms: return ""
    
    al_atom = next((a for a in atoms if a['s'] == 'Al'), None)
    if not al_atom: return ""
    
    cx_map = {'xy': 'x', 'xz': 'x', 'yz': 'y'}
    cy_map = {'xy': 'y', 'xz': 'z', 'yz': 'z'}
    cz_map = {'xy': 'z', 'xz': 'y', 'yz': 'x'}
    
    if zoom:
        filtered_atoms = [a for a in atoms if 
                         abs(a['x'] - al_atom['x']) < zoom and 
                         abs(a['y'] - al_atom['y']) < zoom and
                         abs(a['z'] - al_atom['z']) < zoom]
        ref_x, ref_y = al_atom[cx_map[view]], al_atom[cy_map[view]]
        current_scale = scale * 2.5
    else:
        filtered_atoms = atoms
        # Fixed reference point for unzoomed views
        if view == 'xy':
            ref_x, ref_y = 20, 30
        else: # xz or yz
            ref_x, ref_y = 20, 3.5
        current_scale = scale

    content = f'<g transform="translate({x_off}, {y_off})">\n'
    content += f'<text x="0" y="-15" font-family="Arial" font-size="14" font-weight="bold" fill="#333">{title}</text>\n'
    
    box_w = 350
    box_h = 300
    content += f'<rect x="-10" y="-10" width="{box_w}" height="{box_h}" fill="none" stroke="#ddd" stroke-width="1"/>\n'
    
    sorted_atoms = sorted(filtered_atoms, key=lambda a: a[cz_map[view]])
    
    for a in sorted_atoms:
        vx = (a[cx_map[view]] - ref_x) * current_scale + (box_w/2 if zoom else 20)
        vy = (a[cy_map[view]] - ref_y) * current_scale + (box_h/2 if zoom else 20)
        
        if zoom and (vx < 0 or vx > box_w-20 or vy < 0 or vy > box_h-20): continue
        if not zoom and (vx < 0 or vx > box_w-20 or vy < 0 or vy > box_h-20): continue

        color = "#888"
        r = 3
        opacity = 0.3
        if a['s'] == 'Al': color, r, opacity = "#e74c3c", 8, 1.0
        elif a['s'] == 'Cl': color, r, opacity = "#27ae60", 7, 1.0
        elif zoom: opacity = 0.8
        
        content += f'  <circle cx="{vx}" cy="{vy}" r="{r}" fill="{color}" stroke="#000" stroke-width="0.5" opacity="{opacity}"/>\n'
    content += "</g>\n"
    return content

configs = [
    ('c1', 'Original c1'),
    ('c1_rot90', 'c1 Rotated 90'),
    ('c1_flip', 'c1 Inverted'),
    ('c1_shift', 'c1 Shifted 1.4A'),
    ('c1_diag', 'c1 Diagonal 45')
]

svg_parts = []
y_cursor = 60
row_height = 380
col_width = 380

for folder, name in configs:
    atoms = parse_atoms(f'{folder}/pw.out', find_first=False)
    if not atoms: continue
    
    svg_parts.append(get_svg_view(atoms, f"{name} - Cross-section", 20, y_cursor, view='xy'))
    svg_parts.append(get_svg_view(atoms, f"Top View", col_width, y_cursor, view='xz'))
    svg_parts.append(get_svg_view(atoms, f"Close-up (XZ)", col_width*2, y_cursor, view='xz', zoom=5.0))
    
    y_cursor += row_height

with open('c1_subconfig_comparison.svg', 'w') as f:
    f.write(f'<svg width="{col_width*3 + 100}" height="{y_cursor}" xmlns="http://www.w3.org/2000/svg">\n')
    f.write('<rect width="100%" height="100%" fill="white"/>\n')
    for part in svg_parts: f.write(part)
    f.write('</svg>')

print("Generated updated c1_subconfig_comparison.svg with fixed coordinates.")

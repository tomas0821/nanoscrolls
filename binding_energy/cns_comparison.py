import os
import re

def parse_atoms(filepath, find_first=True, from_in_file=False):
    if not os.path.exists(filepath): return []
    with open(filepath, 'r') as f:
        content = f.read()
    
    if from_in_file:
        # Simple parser for pw.in
        matches = list(re.finditer(r"ATOMIC_POSITIONS\s+\(?([^\)\n]+)\)?", content))
    else:
        # Simple parser for pw.out
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

def get_svg_group(atoms, title, x_off, y_off, scale=10):
    if not atoms: 
        return f'<g transform="translate({x_off}, {y_off})"><text y="50" font-family="Arial">No Data</text></g>'
    
    # Use a shared reference frame for all plots
    ref_x, ref_y = 15, 15
    pad = 40
    
    content = f'<g transform="translate({x_off}, {y_off})">\n'
    content += f'<text x="0" y="-15" font-family="Arial" font-size="16" font-weight="bold" fill="#333">{title}</text>\n'
    
    # Depth sort
    sorted_atoms = sorted(atoms, key=lambda a: a['z'])
    
    for a in sorted_atoms:
        cx = (a['x'] - ref_x) * scale + pad
        cy = (a['y'] - ref_y) * scale + pad
        color = "#666666"
        r = 2.5
        opacity = 0.4
        if a['s'] == 'Al': color, r, opacity = "#e74c3c", 7, 1.0  # Red
        elif a['s'] == 'Cl': color, r, opacity = "#27ae60", 6, 1.0 # Green
        
        content += f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" stroke="#000" stroke-width="0.3" opacity="{opacity}"/>\n'
    content += "</g>\n"
    return content

configs = [
    ('pure_cns', 'Pristine CNS'),
    ('c1', 'Config 1 (c1)'),
    ('c2', 'Config 2 (c2)'),
    ('c3', 'Config 3 (c3)')
]

svg_parts = []
y_cursor = 60
row_height = 320
col_width = 450

for folder, name in configs:
    # Path for initial is the pw.in file
    init_atoms = parse_atoms(f'{folder}/pw.in', find_first=True, from_in_file=True)
    # Path for final is the pw.out file (last step)
    final_atoms = parse_atoms(f'{folder}/pw.out', find_first=False, from_in_file=False)
    
    svg_parts.append(get_svg_group(init_atoms, f"{name} - Initial", 30, y_cursor))
    
    status_label = "Final (Converged)" if folder != 'c2' else "Latest (Running)"
    svg_parts.append(get_svg_group(final_atoms, f"{name} - {status_label}", col_width, y_cursor))
    
    y_cursor += row_height

with open('cns_comparison_final.svg', 'w') as f:
    f.write(f'<svg width="{col_width*2 + 100}" height="{y_cursor}" xmlns="http://www.w3.org/2000/svg">\n')
    f.write('<rect width="100%" height="100%" fill="#fdfdfd"/>\n')
    for part in svg_parts: f.write(part)
    f.write('</svg>')

print("Generated cns_comparison_final.svg")

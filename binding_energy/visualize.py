import os

def parse_pw_in(filepath):
    atoms = []
    if not os.path.exists(filepath): return []
    with open(filepath, 'r') as f:
        lines = f.readlines()
        pos_start = -1
        unit = "angstrom"
        for i, line in enumerate(lines):
            if "ATOMIC_POSITIONS" in line:
                pos_start = i + 1
                if "alat" in line.lower():
                    unit = "alat"
                break
        if pos_start == -1: return []
        
        for line in lines[pos_start:]:
            parts = line.split()
            if len(parts) < 4: break
            try:
                # Scale by 50 if unit is alat for consistent visualization
                scale = 50.0 if unit == "alat" else 1.0
                atoms.append({
                    'symbol': parts[0],
                    'x': float(parts[1]) * scale,
                    'y': float(parts[2]) * scale,
                    'z': float(parts[3]) * scale
                })
            except ValueError:
                break
    return atoms

def get_svg_content(atoms, view='xy'):
    if not atoms: return "", 0, 0
    
    padding = 20
    if view == 'xy':
        coords = [(a['x'], a['y'], a['symbol'], a['z']) for a in atoms]
    else: # top view
        coords = [(a['x'], a['z'], a['symbol'], a['y']) for a in atoms]

    min_x = min(c[0] for c in coords)
    max_x = max(c[0] for c in coords)
    min_y = min(c[1] for c in coords)
    max_y = max(c[1] for c in coords)
    
    width = (max_x - min_x) * 10 + 2 * padding
    height = (max_y - min_y) * 10 + 2 * padding
    
    # Sort by depth for simple occlusion
    sorted_atoms = sorted(atoms, key=lambda a: a['z' if view == 'xy' else 'y'])

    content = ""
    for a in sorted_atoms:
        cx = (a['x'] - min_x) * 10 + padding
        cy = (a['y' if view == 'xy' else 'z'] - min_y) * 10 + padding
        
        color = "#444444" 
        r = 2.5
        opacity = 0.7
        if a['symbol'] == 'Al':
            color = "red"
            r = 6
            opacity = 1.0
        elif a['symbol'] == 'Cl':
            color = "green"
            r = 5
            opacity = 1.0
        
        content += f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" stroke="black" stroke-width="0.3" opacity="{opacity}"/>\n'
    
    return content, width, height

configs = [
    ('pure_cns', 'Pristine CNS (Natural State)'),
    ('c1', 'Configuration 1'),
    ('c2', 'Configuration 2'),
    ('c3', 'Configuration 3')
]

all_views = []
max_w = 0
total_h = 0

for folder, display_name in configs:
    atoms = parse_pw_in(f'{folder}/pw.in')
    if not atoms: continue
    
    side_svg, sw, sh = get_svg_content(atoms, 'xy')
    top_svg, tw, th = get_svg_content(atoms, 'xz')
    
    all_views.append({'name': display_name, 'side': side_svg, 'sw': sw, 'sh': sh, 'top': top_svg, 'tw': tw, 'th': th})
    max_w = max(max_w, sw + tw + 50)
    total_h += max(sh, th) + 60

with open('combined.svg', 'w') as f:
    f.write(f'<svg width="{max_w + 40}" height="{total_h}" xmlns="http://www.w3.org/2000/svg">\n')
    f.write('<rect width="100%" height="100%" fill="white"/>\n')
    
    current_y = 30
    for v in all_views:
        f.write(f'<text x="20" y="{current_y-10}" font-family="Arial" font-size="16" font-weight="bold">{v["name"]}</text>\n')
        # Side View
        f.write(f'<g transform="translate(20, {current_y})">\n')
        f.write(f'<text x="0" y="-5" font-family="Arial" font-size="12">Side View (XY)</text>\n')
        f.write(v['side'])
        f.write('</g>\n')
        
        # Top View
        f.write(f'<g transform="translate({v["sw"] + 50}, {current_y})">\n')
        f.write(f'<text x="0" y="-5" font-family="Arial" font-size="12">Top View (XZ)</text>\n')
        f.write(v['top'])
        f.write('</g>\n')
        
        current_y += max(v['sh'], v['th']) + 60
    
    f.write('</svg>')
print("Generated combined.svg")

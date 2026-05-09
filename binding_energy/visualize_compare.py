import os
import re

def parse_pw_in(filepath):
    atoms = []
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r') as f:
        lines = f.readlines()
    pos_start = -1
    for i, line in enumerate(lines):
        if "ATOMIC_POSITIONS" in line:
            pos_start = i + 1
            break
    if pos_start == -1:
        return []
    for line in lines[pos_start:]:
        parts = line.split()
        if len(parts) < 4:
            break
        try:
            atoms.append({'symbol': parts[0],
                          'x': float(parts[1]),
                          'y': float(parts[2]),
                          'z': float(parts[3])})
        except ValueError:
            break
    return atoms

def parse_last_positions(pw_out):
    """Return atoms from the last ATOMIC_POSITIONS block in pw.out."""
    if not os.path.exists(pw_out):
        return []
    with open(pw_out, 'r') as f:
        lines = f.readlines()
    # find all occurrences
    starts = [i+1 for i, l in enumerate(lines) if 'ATOMIC_POSITIONS' in l]
    if not starts:
        return []
    pos_start = starts[-1]
    atoms = []
    for line in lines[pos_start:]:
        parts = line.split()
        if len(parts) < 4:
            break
        if not re.match(r'^[A-Z][a-z]?$', parts[0]):
            break
        try:
            atoms.append({'symbol': parts[0],
                          'x': float(parts[1]),
                          'y': float(parts[2]),
                          'z': float(parts[3])})
        except ValueError:
            break
    return atoms

def atoms_to_svg(atoms, view='xy'):
    """Return (svg_content, width, height)."""
    if not atoms:
        return '<text x="10" y="30" font-family="Arial" font-size="12" fill="gray">no data</text>', 200, 60

    padding = 20
    if view == 'xy':
        proj = [(a['x'], a['y'], a['z'], a['symbol']) for a in atoms]
    else:
        proj = [(a['x'], a['z'], a['y'], a['symbol']) for a in atoms]

    min_x = min(p[0] for p in proj)
    min_y = min(p[1] for p in proj)
    max_x = max(p[0] for p in proj)
    max_y = max(p[1] for p in proj)

    scale = 8.0
    width  = (max_x - min_x) * scale + 2 * padding
    height = (max_y - min_y) * scale + 2 * padding

    sorted_proj = sorted(proj, key=lambda p: p[2])

    content = ""
    for px, py, _, sym in sorted_proj:
        cx = (px - min_x) * scale + padding
        cy = (py - min_y) * scale + padding
        if sym == 'Al':
            color, r, op = 'red', 6, 1.0
        elif sym == 'Cl':
            color, r, op = 'green', 4, 1.0
        else:
            color, r, op = '#555555', 2, 0.6
        content += (f'  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" '
                    f'fill="{color}" stroke="black" stroke-width="0.3" opacity="{op}"/>\n')
    return content, width, height

configs = [
    ('c1',       'Config 1 (AlCl₄⁻ site 1)'),
    ('c2',       'Config 2 (AlCl₄⁻ site 2)'),
    ('c3',       'Config 3 (AlCl₄⁻ site 3)'),
    ('pure_cns', 'Pristine CNS'),
]

rows = []
max_total_w = 0
total_h = 0
ROW_GAP = 70
COL_GAP = 30

for folder, label in configs:
    ini  = parse_pw_in(f'{folder}/pw.in')
    cur  = parse_last_positions(f'{folder}/pw.out')

    ini_xy, iw_xy, ih_xy = atoms_to_svg(ini, 'xy')
    ini_xz, iw_xz, ih_xz = atoms_to_svg(ini, 'xz')
    cur_xy, cw_xy, ch_xy = atoms_to_svg(cur, 'xy')
    cur_xz, cw_xz, ch_xz = atoms_to_svg(cur, 'xz')

    row_h   = max(ih_xy, ih_xz, ch_xy, ch_xz)
    row_w   = iw_xy + COL_GAP + iw_xz + COL_GAP*3 + cw_xy + COL_GAP + cw_xz

    rows.append({'label': label, 'row_h': row_h, 'row_w': row_w,
                 'ini_xy': ini_xy, 'iw_xy': iw_xy,
                 'ini_xz': ini_xz, 'iw_xz': iw_xz,
                 'cur_xy': cur_xy, 'cw_xy': cw_xy,
                 'cur_xz': cur_xz, 'cw_xz': cw_xz})

    max_total_w = max(max_total_w, row_w)
    total_h += row_h + ROW_GAP

SVG_W = max_total_w + 80
SVG_H = total_h + 40

lines = []
lines.append(f'<svg width="{SVG_W:.0f}" height="{SVG_H:.0f}" xmlns="http://www.w3.org/2000/svg">')
lines.append('<rect width="100%" height="100%" fill="white"/>')

# Column headers
lines.append('<text x="40"  y="22" font-family="Arial" font-size="13" font-weight="bold" fill="#333">Initial — Side (XY)</text>')
lines.append('<text x="40"  y="38" font-family="Arial" font-size="11" fill="#888">from pw.in</text>')

current_y = 55
for row in rows:
    x0 = 40
    # Label
    lines.append(f'<text x="{x0}" y="{current_y - 6}" font-family="Arial" font-size="14" font-weight="bold">{row["label"]}</text>')

    # Divider line between initial/current
    divider_x = x0 + row['iw_xy'] + COL_GAP + row['iw_xz'] + COL_GAP

    # Initial side
    lines.append(f'<g transform="translate({x0},{current_y})">')
    lines.append(f'<text x="0" y="-4" font-family="Arial" font-size="10" fill="#666">Side (XY)</text>')
    lines.append(row['ini_xy'])
    lines.append('</g>')

    x1 = x0 + row['iw_xy'] + COL_GAP
    # Initial top
    lines.append(f'<g transform="translate({x1},{current_y})">')
    lines.append(f'<text x="0" y="-4" font-family="Arial" font-size="10" fill="#666">Top (XZ)</text>')
    lines.append(row['ini_xz'])
    lines.append('</g>')

    # Divider
    lines.append(f'<line x1="{divider_x}" y1="{current_y - 20}" x2="{divider_x}" y2="{current_y + row["row_h"]}" '
                 f'stroke="#aaa" stroke-width="1.5" stroke-dasharray="6,3"/>')
    lines.append(f'<text x="{divider_x + 6}" y="{current_y - 4}" font-family="Arial" font-size="10" fill="#666">Current — Side (XY)</text>')

    x2 = divider_x + COL_GAP
    # Current side
    lines.append(f'<g transform="translate({x2},{current_y})">')
    lines.append(row['cur_xy'])
    lines.append('</g>')

    x3 = x2 + row['cw_xy'] + COL_GAP
    # Current top
    lines.append(f'<g transform="translate({x3},{current_y})">')
    lines.append(f'<text x="0" y="-4" font-family="Arial" font-size="10" fill="#666">Top (XZ)</text>')
    lines.append(row['cur_xz'])
    lines.append('</g>')

    # Separator
    sep_y = current_y + row['row_h'] + ROW_GAP // 2
    lines.append(f'<line x1="20" y1="{sep_y}" x2="{SVG_W-20:.0f}" y2="{sep_y}" stroke="#ddd" stroke-width="1"/>')

    current_y += row['row_h'] + ROW_GAP

lines.append('</svg>')

with open('comparison.svg', 'w') as f:
    f.write('\n'.join(lines))

print("Generated comparison.svg")
for row in rows:
    ini = parse_pw_in(f'{row["label"].split()[0].lower()}/pw.in') if False else None
    print(f"  {row['label']}")

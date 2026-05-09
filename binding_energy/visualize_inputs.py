import os

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

def atoms_to_svg(atoms, view='xy'):
    if not atoms:
        return '<text x="10" y="30" font-size="12" fill="gray">no data</text>', 200, 60
    padding = 20
    if view == 'xy':
        proj = [(a['x'], a['y'], a['z'], a['symbol']) for a in atoms]
    else:
        proj = [(a['x'], a['z'], a['y'], a['symbol']) for a in atoms]
    min_x = min(p[0] for p in proj)
    min_y = min(p[1] for p in proj)
    scale = 7.0
    width  = (max(p[0] for p in proj) - min_x) * scale + 2 * padding
    height = (max(p[1] for p in proj) - min_y) * scale + 2 * padding
    content = ""
    for px, py, _, sym in sorted(proj, key=lambda p: p[2]):
        cx = (px - min_x) * scale + padding
        cy = (py - min_y) * scale + padding
        if sym == 'Al':
            color, r, op = 'red', 7, 1.0
        elif sym == 'Cl':
            color, r, op = 'green', 5, 1.0
        else:
            color, r, op = '#555', 2, 0.55
        content += (f'  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" '
                    f'fill="{color}" stroke="black" stroke-width="0.3" opacity="{op}"/>\n')
    return content, width, height

configs = [
    ('c1',       'c1 — Site 1'),
    ('c2',       'c2 — Site 2'),
    ('c3',       'c3 — Site 3'),
    ('pure_cns', 'pure_cns'),
]

GAP = 40
LABEL_H = 30
rows = []
for folder, label in configs:
    atoms = parse_pw_in(f'{folder}/pw.in')
    al = [a for a in atoms if a['symbol'] == 'Al']
    cl = [a for a in atoms if a['symbol'] == 'Cl']
    print(f"{label}: {len(atoms)} atoms  |  Al={[round(a['x'],2) for a in al]}  Cl_count={len(cl)}")
    sv, sw, sh = atoms_to_svg(atoms, 'xy')
    tv, tw, th = atoms_to_svg(atoms, 'xz')
    rows.append({'label': label, 'sv': sv, 'sw': sw, 'sh': sh, 'tv': tv, 'tw': tw, 'th': th})

col_gap = 30
svg_w = max(r['sw'] + col_gap + r['tw'] for r in rows) + 80
svg_h = sum(max(r['sh'], r['th']) + LABEL_H + GAP for r in rows) + 20

lines = ['<svg width="{:.0f}" height="{:.0f}" xmlns="http://www.w3.org/2000/svg">'.format(svg_w, svg_h),
         '<rect width="100%" height="100%" fill="white"/>']

y = 20
for r in rows:
    row_h = max(r['sh'], r['th'])
    lines.append(f'<text x="40" y="{y + 16}" font-family="Arial" font-size="15" font-weight="bold">{r["label"]}</text>')
    lines.append(f'<text x="{40 + r["sw"]//2}" y="{y + 16}" font-family="Arial" font-size="11" fill="#888" text-anchor="middle">Side (XY)</text>')
    lines.append(f'<text x="{40 + r["sw"] + col_gap + r["tw"]//2}" y="{y + 16}" font-family="Arial" font-size="11" fill="#888" text-anchor="middle">Top (XZ)</text>')
    y += LABEL_H
    lines.append(f'<g transform="translate(40,{y})">{r["sv"]}</g>')
    lines.append(f'<g transform="translate({40 + r["sw"] + col_gap},{y})">{r["tv"]}</g>')
    y += row_h + GAP
    lines.append(f'<line x1="20" y1="{y - GAP//2}" x2="{svg_w-20:.0f}" y2="{y - GAP//2}" stroke="#ddd" stroke-width="1"/>')

lines.append('</svg>')
with open('inputs_check.svg', 'w') as f:
    f.write('\n'.join(lines))
print("\nGenerated inputs_check.svg")

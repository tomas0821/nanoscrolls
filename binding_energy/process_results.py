import os
import re

RY_TO_EV = 13.605693

def get_total_energy(folder):
    path = os.path.join(folder, 'pw.out')
    if not os.path.exists(path):
        return None
    
    energy = None
    is_converged = False
    with open(path, 'r') as f:
        for line in f:
            if 'total energy' in line:
                # Format: !    total energy              =   -3539.80660880 Ry
                # or:          total energy              =   -3539.80660880 Ry
                match = re.search(r'=\s+([-.\d]+)\s+Ry', line)
                if match:
                    energy = float(match.group(1))
                    is_converged = '!' in line
    
    if energy is not None and not is_converged:
        print(f"Warning: Energy for {folder} is not from a converged SCF/Relaxation step (taking last available).")
    return energy

def create_plot_svg(results, filename):
    # results is a list of (name, energy_ev)
    if not results: return
    
    width = 600
    height = 400
    margin = 60
    
    # Calculate scale
    energies = [r[1] for r in results]
    min_e = min(energies + [0])
    max_e = max(energies + [0])
    
    # Ensure some range for the plot
    if abs(max_e - min_e) < 0.001:
        max_e += 0.5
        min_e -= 0.5
    
    # Add buffer to range
    range_e = max_e - min_e
    max_e += range_e * 0.1
    min_e -= range_e * 0.1
    range_e = max_e - min_e

    def to_y(val):
        return height - margin - (val - min_e) * (height - 2*margin) / range_e

    y_zero = to_y(0)
    
    with open(filename, 'w') as f:
        f.write(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\n')
        f.write('<rect width="100%" height="100%" fill="white"/>\n')
        
        # Grid and axes
        f.write(f'<line x1="{margin}" y1="{margin}" x2="{margin}" y2="{height-margin}" stroke="black" stroke-width="2"/>\n')
        f.write(f'<line x1="{margin}" y1="{y_zero}" x2="{width-margin}" y2="{y_zero}" stroke="gray" stroke-width="1" stroke-dasharray="5,5"/>\n')
        
        # Labels
        f.write(f'<text x="{width/2}" y="{height-15}" font-family="Arial" font-size="14" text-anchor="middle">Configuration</text>\n')
        f.write(f'<text x="20" y="{height/2}" font-family="Arial" font-size="14" text-anchor="middle" transform="rotate(-90, 20, {height/2})">Binding Energy (eV)</text>\n')
        
        # Bars
        bar_width = (width - 2*margin) / (len(results) * 1.5)
        spacing = (width - 2*margin) / len(results)
        
        for i, (name, val) in enumerate(results):
            x = margin + spacing * (i + 0.25)
            y_val = to_y(val)
            
            h_bar = abs(y_val - y_zero)
            y_start = min(y_val, y_zero)
            
            color = "#3498db" if val < 0 else "#e74c3c"
            f.write(f'  <rect x="{x}" y="{y_start}" width="{bar_width}" height="{h_bar}" fill="{color}" stroke="black" stroke-width="1"/>\n')
            f.write(f'  <text x="{x + bar_width/2}" y="{height-margin+20}" font-family="Arial" font-size="12" text-anchor="middle">{name}</text>\n')
            # Energy label above/below bar
            y_text = y_val - 10 if val > 0 else y_val + 20
            f.write(f'  <text x="{x + bar_width/2}" y="{y_text}" font-family="Arial" font-size="10" text-anchor="middle" font-weight="bold">{val:.3f}</text>\n')

        f.write('</svg>')

# Main Execution
ref_cns = get_total_energy('pure_cns')
ref_mol = get_total_energy('alcl4_molecule')

print("--- Total Energies (Ry) ---")
print(f"Reference CNS: {ref_cns}")
print(f"Reference AlCl4: {ref_mol}")

configs = ['c1', 'c2', 'c3']
final_results = []

print("\n--- Binding Energies ---")
print(f"{'Config':<10} | {'E_tot (Ry)':<15} | {'E_bind (eV)':<15}")
print("-" * 45)

for cfg in configs:
    e_tot = get_total_energy(cfg)
    if e_tot and ref_cns and ref_mol:
        e_bind_ry = e_tot - (ref_cns + ref_mol)
        e_bind_ev = e_bind_ry * RY_TO_EV
        print(f"{cfg:<10} | {e_tot:<15.6f} | {e_bind_ev:<15.4f}")
        final_results.append((cfg, e_bind_ev))
    else:
        status = "Pending" if not e_tot else "Missing Ref"
        print(f"{cfg:<10} | {status}")

if final_results:
    create_plot_svg(final_results, 'binding_energies.svg')
    print("\nGenerated binding_energies.svg")
else:
    print("\nNo results to plot yet.")

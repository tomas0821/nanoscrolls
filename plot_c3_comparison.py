import os
import re
import matplotlib.pyplot as plt

def extract_data(file_list):
    energies, forces = [], []
    for filepath in file_list:
        if not os.path.exists(filepath): continue
        with open(filepath, 'r') as f:
            content = f.read()
        e = re.findall(r"!    total energy\s+=\s+([-.\d]+)\s+Ry", content)
        f_list = re.findall(r"Total force\s+=\s+([-.\d]+)\s+Total SCF", content)
        energies.extend([float(x) for x in e])
        forces.extend([float(x) for x in f_list])
    return energies, forces

ref_energy = -3896.987915

c3_data = {
    'c3_diag': ['binding_energy/c3_diag.out', 'binding_energy/c3_diag/pw.out'],
    'c3_flip': ['binding_energy/c3_flip.out', 'binding_energy/c3_flip/pw.out'],
    'c3_rot90': ['binding_energy/c3_rot90.out', 'binding_energy/c3_rot90/pw.out']
}

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 18), dpi=200)
colors = {'c3_diag': '#e74c3c', 'c3_flip': '#2ecc71', 'c3_rot90': '#3498db'}

for label, files in c3_data.items():
    e, f = extract_data(files)
    if not e: continue
    de = [abs(e[i] - e[i-1]) for i in range(1, len(e))]
    
    ax1.plot(e, label=label, color=colors[label], marker='o', markersize=2, alpha=0.7)
    ax2.plot(f, label=label, color=colors[label], marker='x', markersize=2, linestyle='--', alpha=0.6)
    ax3.plot(de, label=label, color=colors[label], marker='s', markersize=2, linestyle=':', alpha=0.5)

# 1. Total Energy
ax1.axhline(y=ref_energy, color='black', linestyle='--', alpha=0.5, label='Binding Threshold')
ax1.set_title('Energy Comparison of c3 Orientations', fontsize=14, fontweight='bold')
ax1.set_ylabel('Total Energy (Ry)')
ax1.legend(); ax1.grid(True, alpha=0.3)

# 2. Forces (Log)
ax2.axhline(y=0.001, color='green', linestyle='-', lw=2, label='Conv Target (0.001)')
ax2.set_title('Force Convergence (Threshold: 0.001)', fontsize=14, fontweight='bold')
ax2.set_ylabel('Force (Ry/au)')
ax2.set_yscale('log'); ax2.legend(); ax2.grid(True, which="both", alpha=0.2)

# 3. Energy Change (Log)
ax3.axhline(y=0.0001, color='green', linestyle='-', lw=2, label='Conv Target (0.0001)')
ax3.set_title('Energy Change Convergence (Threshold: 0.0001)', fontsize=14, fontweight='bold')
ax3.set_ylabel('|Delta E| (Ry)')
ax3.set_yscale('log'); ax3.set_xlabel('Structural Steps'); ax3.legend(); ax3.grid(True, which="both", alpha=0.2)

plt.tight_layout()
plt.savefig('c3_subconfig_comparison.png')
print("Generated c3_subconfig_comparison.png with all Convergence Thresholds.")

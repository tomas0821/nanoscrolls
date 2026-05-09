import os
import re
import numpy as np
import matplotlib.pyplot as plt

def extract_data(filepath):
    if not os.path.exists(filepath): return [], []
    with open(filepath, 'r') as f:
        content = f.read()
    e = re.findall(r"!    total energy\s+=\s+([-.\d]+)\s+Ry", content)
    f = re.findall(r"Total force\s+=\s+([-.\d]+)\s+Total SCF", content)
    return [float(x) for x in e], [float(x) for x in f]

files = ['binding_energy/pw_c2.out', 'binding_energy/c2/pw.out']
all_e, all_f = [], []
for f in files:
    e, f_list = extract_data(f)
    all_e.extend(e)
    all_f.extend(f_list)

if all_e:
    # Calculate Delta Energy
    delta_e = [abs(all_e[i] - all_e[i-1]) for i in range(1, len(all_e))]
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15), dpi=200)
    
    # 1. Total Energy
    ax1.plot(all_e, color='tab:blue', marker='o', markersize=4, label='Total Energy')
    ax1.axhline(y=-3896.987915, color='black', linestyle='--', alpha=0.5, label='Binding Threshold')
    ax1.set_ylabel('Energy (Ry)')
    ax1.set_title('c2: Total Energy History', fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. Total Force (Log Scale)
    ax2.plot(all_f, color='tab:red', marker='x', markersize=4, linestyle='--', label='Total Force')
    ax2.axhline(y=0.001, color='green', linestyle='-', lw=2, label='Target (0.001)')
    ax2.set_ylabel('Force (Ry/au)')
    ax2.set_yscale('log')
    ax2.set_title('c2: Force Convergence', fontweight='bold')
    ax2.legend()
    ax2.grid(True, which="both", alpha=0.2)

    # 3. Delta Energy (Log Scale)
    ax3.plot(delta_e, color='tab:purple', marker='s', markersize=4, linestyle=':', label='|dE| per step')
    ax3.axhline(y=0.0001, color='green', linestyle='-', lw=2, label='Target (0.0001)')
    ax3.set_ylabel('|Delta E| (Ry)')
    ax3.set_yscale('log')
    ax3.set_xlabel('Structural Step')
    ax3.set_title('c2: Energy Change Convergence', fontweight='bold')
    ax3.legend()
    ax3.grid(True, which="both", alpha=0.2)

    plt.tight_layout()
    plt.savefig('c2_recent_progress.png')
    print("Generated c2_recent_progress.png with all Convergence Thresholds.")

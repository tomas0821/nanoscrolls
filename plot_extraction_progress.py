import os
import re
import matplotlib.pyplot as plt

def extract_data(filepath):
    if not os.path.exists(filepath): return [], []
    with open(filepath, 'r') as f:
        content = f.read()
    e = re.findall(r"!    total energy\s+=\s+([-.\d]+)\s+Ry", content)
    f = re.findall(r"Total force\s+=\s+([-.\d]+)\s+Total SCF", content)
    return [float(x) for x in e], [float(x) for x in f]

ref_energy = -3896.987915

def plot_triple(axes, path, title):
    e, f = extract_data(path)
    if not e:
        for ax in axes: ax.text(0.5, 0.5, "No Data", ha='center')
        return
    
    de = [abs(e[i] - e[i-1]) for i in range(1, len(e))]
    
    # Energy
    axes[0].plot(e, color='tab:blue', marker='o', markersize=2)
    axes[0].axhline(y=ref_energy, color='black', linestyle='--', alpha=0.5)
    axes[0].set_title(title, fontweight='bold'); axes[0].set_ylabel('E (Ry)')
    
    # Forces (Log)
    axes[1].plot(f, color='tab:red', marker='x', markersize=2, linestyle='--')
    axes[1].axhline(y=0.001, color='green', linestyle='-', lw=2)
    axes[1].set_yscale('log'); axes[1].set_ylabel('Force')
    
    # dE (Log)
    axes[2].plot(de, color='tab:purple', marker='s', markersize=2, linestyle=':')
    axes[2].axhline(y=0.0001, color='green', linestyle='-', lw=2)
    axes[2].set_yscale('log'); axes[2].set_ylabel('|dE|')

fig, axes = plt.subplots(3, 2, figsize=(18, 15), dpi=200)

plot_triple(axes[:, 0], 'extraction_path/step_2/pw.out', "Radial Step 2")
plot_triple(axes[:, 1], 'axial_extraction/step_2/pw.out', "Axial Step 2")

plt.tight_layout()
plt.savefig('extraction_progress_trends.png')
print("Generated extraction_progress_trends.png with Triple Panels.")

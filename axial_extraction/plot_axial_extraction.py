import matplotlib.pyplot as plt

# Converged Data Points
# (Z-position of Al, Total Energy in Ry)
z_pos = [11.22, 12.22, 13.22]
energies = [-3886.31630129, -3886.54756335, -3886.54448333]

# Normalize energy relative to Step 2 (most stable so far)
min_e = min(energies)
rel_energies_ev = [(e - min_e) * 13.605693 for e in energies]

plt.figure(figsize=(10, 6), dpi=200)

# Plot Relative Energy
plt.plot(z_pos, rel_energies_ev, marker='o', markersize=8, linestyle='-', color='#e67e22', linewidth=2, label='Extraction Profile')

# Add Scroll Boundaries (from 8.8 to 14.87)
plt.axvspan(8.8, 14.87, color='gray', alpha=0.2, label='CNS Segment')
plt.axvline(x=14.87, color='red', linestyle='--', label='Exit Mouth')

plt.title('Axial Extraction Energy Barrier (Steps 1-3)', fontsize=14, fontweight='bold')
plt.xlabel('Aluminum Z-position ($\AA$)', fontsize=12)
plt.ylabel('Relative Energy (eV)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.4)
plt.legend()

# Annotate points
for z, e in zip(z_pos, rel_energies_ev):
    plt.annotate(f'{e:.3f} eV', xy=(z, e), xytext=(5, 5), textcoords='offset points')

plt.tight_layout()
plt.savefig('axial_extraction_energy.png')
print("Generated: axial_extraction_energy.png")

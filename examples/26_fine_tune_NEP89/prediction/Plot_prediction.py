import sys
import matplotlib.pyplot as plt
import numpy as np
# from cycler import cycler

# custom_colors = ['#8FA2CD', '#F8BC7E', '#A9CA70', '#F09BA0', '#9D9EA3', '#B7B7EB']
# plt.rcParams['axes.prop_cycle'] = cycler(color=custom_colors)

# Load data
energy_data = np.loadtxt('energy_train.out')
force_data = np.loadtxt('force_train.out')
stress_data = np.loadtxt('stress_train.out')

# Filter out rows with invalid stress data
valid_rows = ~np.any(np.abs(stress_data[:, :12]) > 1e6, axis=1)
stress_data = stress_data[valid_rows]

# Function to calculate RMSE
def calculate_rmse(pred, actual):
    return np.sqrt(np.mean((pred - actual) ** 2))

# Function to calculate dynamic axis limits
def calculate_limits(train_data, padding=0.08):
    data_min = np.min(train_data)
    data_max = np.max(train_data)
    data_range = data_max - data_min
    return data_min - padding * data_range, data_max + padding * data_range

# Create a subplot with 1 row and 3 columns
fig, axs = plt.subplots(1, 3, figsize=(12, 3.3), dpi=100)

# Plotting the train_data figure
xmin_energy, xmax_energy = calculate_limits(energy_data[:, 1])
axs[0].set_xlim(xmin_energy, xmax_energy)
axs[0].set_ylim(xmin_energy, xmax_energy)
axs[0].plot(energy_data[:, 1], energy_data[:, 0], '.', markersize=10)
axs[0].plot([xmin_energy, xmax_energy], [xmin_energy, xmax_energy], linewidth=2, color='grey', linestyle='--')
axs[0].set_xlabel('DFT energy (eV/atom)', fontsize=11)
axs[0].set_ylabel('NEP energy (eV/atom)', fontsize=11)
axs[0].legend(['energy'])
axs[0].axis('tight')
axs[0].tick_params(axis='both', labelsize=11)

# Calculate and display RMSE for energy
energy_rmse = calculate_rmse(energy_data[:, 0], energy_data[:, 1]) * 1000
axs[0].text(0.35, 0.08, f'RMSE: {energy_rmse:.2f} meV/atom', transform=axs[0].transAxes, fontsize=11, verticalalignment='center')
axs[0].text(-0.1, 1.03, "(a)", transform=axs[0].transAxes, fontsize=13, va='top', ha='right')

# Plotting the force_data figure
xmin_force, xmax_force = calculate_limits(force_data[:, 3:6].reshape(-1))
axs[1].set_xlim(xmin_force, xmax_force)
axs[1].set_ylim(xmin_force, xmax_force)
axs[1].plot(force_data[:, 3:6], force_data[:, 0:3], '.', markersize=10)
axs[1].plot([xmin_force, xmax_force], [xmin_force, xmax_force], linewidth=2, color='grey', linestyle='--')
axs[1].set_xlabel(r'DFT force (eV/$\mathrm{\AA}$)', fontsize=11)
axs[1].set_ylabel(r'NEP force (eV/$\mathrm{\AA}$)', fontsize=11)
axs[1].tick_params(axis='both', labelsize=11)
axs[1].legend(['fx', 'fy', 'fz'])
axs[1].axis('tight')

# Calculate and display RMSE for forces
force_rmse = [calculate_rmse(force_data[:, i], force_data[:, i + 3]) for i in range(3)]
mean_force_rmse = np.mean(force_rmse) * 1000
axs[1].text(0.35, 0.08, rf'RMSE: {mean_force_rmse:.2f} meV/$\mathrm{{\AA}}$', transform=axs[1].transAxes, fontsize=11, verticalalignment='center')
axs[1].text(-0.1, 1.03, "(b)", transform=axs[1].transAxes, fontsize=13, va='top', ha='right')

# Plotting the stress figure
xmin_stress, xmax_stress = calculate_limits(stress_data[:, 6:12].reshape(-1))
axs[2].set_xlim(xmin_stress, xmax_stress)
axs[2].set_ylim(xmin_stress, xmax_stress)
axs[2].plot(stress_data[:, 6:12], stress_data[:, 0:6], '.', markersize=10)
axs[2].plot([xmin_stress, xmax_stress], [xmin_stress, xmax_stress], linewidth=2, color='grey', linestyle='--')
axs[2].set_xlabel('DFT stress (GPa)', fontsize=11)
axs[2].set_ylabel('NEP stress (GPa)', fontsize=11)
axs[2].tick_params(axis='both', labelsize=11)
axs[2].legend(['xx', 'yy', 'zz', 'xy', 'yz', 'zx'])
axs[2].axis('tight')

# Calculate and display RMSE for stresses
stress_rmse = [calculate_rmse(stress_data[:, i], stress_data[:, i + 6]) for i in range(6)]
mean_stress_rmse = np.mean(stress_rmse)
axs[2].text(0.35, 0.08, f'RMSE: {mean_stress_rmse:.4f} GPa', transform=axs[2].transAxes, fontsize=11, verticalalignment='center')
axs[2].text(-0.1, 1.03, "(c)", transform=axs[2].transAxes, fontsize=13, va='top', ha='right')

# Adjust layout for better spacing
plt.tight_layout()
fig.subplots_adjust(top=0.968,bottom=0.16, left=0.086,right=0.983,hspace=0.2,wspace=0.25)
plt.savefig('prediction.png', dpi=300)

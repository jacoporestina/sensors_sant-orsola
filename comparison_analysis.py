import matplotlib.pyplot as plt
import os

def plot_shaded_vs_control(means_data, save_dir='plots/shaded_vs_control'):
    """
    Plots the mean values of all variables for control and shaded treatments together, using monthly data.
    Creates separate plots for each month and saves them in a folder structure.

    Parameters:
        means_data (dict): The dictionary containing the data.
        save_dir (str): The directory where plots will be saved. Default is 'plots/shaded_vs_control'.
    """
    # Create the save directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Loop through each variable (e.g., temperature, humidity, PAR, etc.)
    for variable, treatments in means_data.items():

        # Extract monthly data for control and shaded treatments
        control_monthly = treatments['control']['month']
        shaded_monthly = treatments['shaded']['month']

        # Loop through each month
        for month in control_monthly.keys():

            # Create a plot for the current month
            plt.figure(figsize=(12, 6))

            # Plot control data for the month
            control_data = control_monthly[month]
            if 'daily' in control_data and 'mean' in control_data['daily'] and not control_data['daily']['mean'].empty:
                plt.plot(control_data['daily']['mean'].index, control_data['daily']['mean'][variable], label=f'Control {month}', color='blue', linestyle='-', linewidth=1)

            # Plot shaded data for the month
            shaded_data = shaded_monthly[month]
            if 'daily' in shaded_data and 'mean' in shaded_data['daily'] and not shaded_data['daily']['mean'].empty:
                plt.plot(shaded_data['daily']['mean'].index, shaded_data['daily']['mean'][variable], label=f'Shaded {month}', color='orange', linestyle='-', linewidth=1)

            # Add labels, title, and legend
            plt.xlabel('Time')
            plt.ylabel(variable.capitalize())
            plt.title(f'Monthly {variable.capitalize()} - Control vs Shaded ({month})')
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.6)

            # Save the plot
            filename = os.path.join(save_dir, f'{variable}_control_vs_shaded_{month}.png')
            print(f"Saving plot to: {filename}")
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()  # Close the plot to free up memory

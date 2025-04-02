import matplotlib.pyplot as plt
import os

def plot_variables(means_data, save_dir='plots'):
    """
    Generates and saves plots for each variable, treatment, and time period in the means_data dictionary.
    Plots are customized for PAR, VPD, temperature, and RH, with specific requirements for monthly, weekly, and daily data.
    Plots are saved in a folder structure that mirrors the dictionary.

    Parameters:
        means_data (dict): The dictionary containing the data.
        save_dir (str): The directory where plots will be saved. Default is 'plots'.
    """
    # Create the save directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Helper function to plot PAR and VPD data
    def plot_par_vpd(data, variable, treatment, data_type, time_period):
        """Plots PAR and VPD data (mean only)."""
        if data_type == 'month' and 'daily' in data and 'mean' in data['daily']:
            plt.plot(data['daily']['mean'].index, data['daily']['mean'][variable], label=f'{treatment.capitalize()} Daily Mean', color='green', linestyle='-', linewidth=1)
        elif data_type in ['week', 'day'] and 'hourly' in data and 'mean' in data['hourly']:
            plt.plot(data['hourly']['mean'].index, data['hourly']['mean'][variable], label=f'{treatment.capitalize()} Hourly Mean', color='green', linestyle='-', linewidth=1)

    # Helper function to plot Temperature and RH data
    def plot_temp_rh(data, variable, treatment, data_type, time_period):
        """Plots Temperature and RH data (mean, max, min)."""
        if data_type == 'month' and 'daily' in data:
            if 'mean' in data['daily']:
                plt.plot(data['daily']['mean'].index, data['daily']['mean'][variable], label=f'{treatment.capitalize()} Daily Mean', color='green', linestyle='-', linewidth=1)
            if 'max' in data['daily']:
                plt.plot(data['daily']['max'].index, data['daily']['max'][variable], label=f'{treatment.capitalize()} Daily Max', color='red', linestyle='--', linewidth=1)
            if 'min' in data['daily']:
                plt.plot(data['daily']['min'].index, data['daily']['min'][variable], label=f'{treatment.capitalize()} Daily Min', color='blue', linestyle='--', linewidth=1)
        elif data_type in ['week', 'day'] and 'hourly' in data:
            if 'mean' in data['hourly']:
                plt.plot(data['hourly']['mean'].index, data['hourly']['mean'][variable], label=f'{treatment.capitalize()} Hourly Mean', color='green', linestyle='-', linewidth=1)
            if 'max' in data['hourly']:
                plt.plot(data['hourly']['max'].index, data['hourly']['max'][variable], label=f'{treatment.capitalize()} Hourly Max', color='red', linestyle='--', linewidth=1)
            if 'min' in data['hourly']:
                plt.plot(data['hourly']['min'].index, data['hourly']['min'][variable], label=f'{treatment.capitalize()} Hourly Min', color='blue', linestyle='--', linewidth=1)

    # Loop through each variable (e.g., temperature, humidity, PAR, etc.)
    for variable, treatments in means_data.items():
        # Create a subfolder for the current variable
        variable_dir = os.path.join(save_dir, variable)
        if not os.path.exists(variable_dir):
            os.makedirs(variable_dir)

        # Loop through each treatment (e.g., control, shaded)
        for treatment, data_types in treatments.items():
            # Create a subfolder for the current treatment
            treatment_dir = os.path.join(variable_dir, treatment)
            if not os.path.exists(treatment_dir):
                os.makedirs(treatment_dir)

            # Loop through each data type (e.g., month, week, day)
            for data_type, time_periods in data_types.items():
                # Create a subfolder for the current data type
                data_type_dir = os.path.join(treatment_dir, data_type)
                if not os.path.exists(data_type_dir):
                    os.makedirs(data_type_dir)

                # Loop through each time period (e.g., 2024-07, 2024-27, 2024-07-01)
                for time_period, data in time_periods.items():
                    # Create a plot for the current variable, treatment, data type, and time period
                    plt.figure(figsize=(12, 6))

                    # Check if the variable is PAR or VPD
                    if variable in ['photosyntheticallyActiveRadiation', 'vaporPressureDeficit']:
                        plot_par_vpd(data, variable, treatment, data_type, time_period)
                    else:
                        # For Temperature and RH
                        plot_temp_rh(data, variable, treatment, data_type, time_period)

                    # Add labels, title, and legend
                    plt.xlabel('Time')
                    plt.ylabel(variable.capitalize())
                    plt.title(f'{data_type.capitalize()} {variable.capitalize()} in {treatment.capitalize()} Conditions ({time_period})')
                    plt.legend()
                    plt.grid(True, linestyle='--', alpha=0.6)

                    # Save the plot
                    filename = os.path.join(data_type_dir, f'{time_period}.png')
                    plt.savefig(filename, dpi=300, bbox_inches='tight')
                    plt.close()  # Close the plot to free up memory
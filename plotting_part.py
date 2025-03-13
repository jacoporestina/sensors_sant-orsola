import matplotlib.pyplot as plt
import os

def plot_variables(means_data, save_dir='plots'):
    """
    Generates and saves plots for each variable and treatment in the means_data dictionary.

    Parameters:
        means_data (dict): The dictionary containing the data.
        save_dir (str): The directory where plots will be saved. Default is 'plots'.
    """
    # Create the save directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Loop through each variable (e.g., temperature, humidity, PAR, etc.)
    for variable, treatments in means_data.items():
        # Loop through each treatment (e.g., control, shaded)
        for treatment, data_types in treatments.items():
            # Loop through each data type (e.g., hourly, daily)
            for data_type, data in data_types.items():
                # Create a plot for the current variable, treatment, and data type
                plt.figure(figsize=(12, 6))
                plt.plot(data.index, data[variable], label=f'{treatment.capitalize()} {variable}', color='blue' if treatment == 'control' else 'red')

                # Add labels, title, and legend
                plt.xlabel('Time')
                plt.ylabel(variable.capitalize())
                plt.title(f'{data_type.capitalize()} {variable.capitalize()} in {treatment.capitalize()} Conditions')
                plt.legend()

                # Save the plot
                filename = f'{save_dir}/{variable}_{treatment}_{data_type}.png'
                plt.savefig(filename, dpi=300, bbox_inches='tight')
                plt.close()  # Close the plot to free up memory
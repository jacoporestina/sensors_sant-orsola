import matplotlib.pyplot as plt
import os

def plot_max_temperature(means_data, save_dir='plots/max_temperature'):
    """
    Plots the maximum temperature values for control and shaded treatments, using monthly, weekly, and daily data.
    Saves plots in respective subfolders.

    Parameters:
        means_data (dict): The dictionary containing the data.
        save_dir (str): The directory where plots will be saved. Default is 'plots/max_temperature'.
    """
    # Create the save directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Create subfolders for monthly, weekly, and daily plots
    monthly_dir = os.path.join(save_dir, 'monthly')
    weekly_dir = os.path.join(save_dir, 'weekly')
    daily_dir = os.path.join(save_dir, 'daily')

    for subdir in [monthly_dir, weekly_dir, daily_dir]:
        if not os.path.exists(subdir):
            os.makedirs(subdir)

    # Extract temperature data
    if 'temperature' not in means_data:
        print("No temperature data found.")
        return

    treatments = means_data['temperature']

    # Extract monthly, weekly, and daily data for control and shaded treatments
    control_monthly = treatments['control']['month']
    shaded_monthly = treatments['shaded']['month']
    control_weekly = treatments['control']['week']
    shaded_weekly = treatments['shaded']['week']
    control_daily = treatments['control']['day']
    shaded_daily = treatments['shaded']['day']

    # Plot monthly data
    for month in control_monthly.keys():
        plt.figure(figsize=(12, 6))

        # Plot control data for the month
        control_data = control_monthly[month]
        if 'daily' in control_data and 'max' in control_data['daily'] and not control_data['daily']['max'].empty:
            plt.plot(control_data['daily']['max'].index, control_data['daily']['max']['temperature'], label=f'Control {month}', color='black', linestyle='-', linewidth=1)

        # Plot shaded data for the month
        shaded_data = shaded_monthly[month]
        if 'daily' in shaded_data and 'max' in shaded_data['daily'] and not shaded_data['daily']['max'].empty:
            plt.plot(shaded_data['daily']['max'].index, shaded_data['daily']['max']['temperature'], label=f'Shaded {month}', color='black', linestyle='--', linewidth=1)

        # Add labels, title, and legend
        plt.xlabel('Time')
        plt.ylabel('Max Temperature')
        plt.title(f'Monthly Max Temperature - Control vs Shaded ({month})')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)

        # Save the plot
        filename = os.path.join(monthly_dir, f'temperature_max_control_vs_shaded_{month}.png')
        print(f"Saving monthly max plot to: {filename}")
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()  # Close the plot to free up memory

    # Plot mweekly data
    for week in control_weekly.keys():
        plt.figure(figsize=(12, 6))

        # Plot control data for the week
        control_data = control_weekly[week]
        if 'hourly' in control_data and 'max' in control_data['hourly'] and not control_data['hourly']['max'].empty:
            plt.plot(control_data['hourly']['max'].index, control_data['hourly']['max']['temperature'], label=f'Control {week}', color='black', linestyle='-', linewidth=1)

        # Plot shaded data for the week
        shaded_data = shaded_weekly[week]
        if 'hourly' in shaded_data and 'max' in shaded_data['hourly'] and not shaded_data['hourly']['max'].empty:
            plt.plot(shaded_data['hourly']['max'].index, shaded_data['hourly']['max']['temperature'], label=f'Shaded {week}', color='black', linestyle='--', linewidth=1)

        # Add labels, title, and legend
        plt.xlabel('Time')
        plt.ylabel('Max Temperature')
        plt.title(f'Weekly Max Temperature - Control vs Shaded ({week})')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)

        # Save the plot
        filename = os.path.join(weekly_dir, f'temperature_max_control_vs_shaded_{week}.png')
        print(f"Saving weekly max plot to: {filename}")
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()  # Close the plot to free up memory

    # Plot mweekly data
    for day in control_daily.keys():
        plt.figure(figsize=(12, 6))

        # Plot control data for the day
        control_data = control_daily[day]
        if 'hourly' in control_data and 'max' in control_data['hourly'] and not control_data['hourly']['max'].empty:
            plt.plot(control_data['hourly']['max'].index, control_data['hourly']['max']['temperature'], label=f'Control {day}', color='black', linestyle='-', linewidth=1)

        # Plot shaded data for the day
        shaded_data = shaded_daily[day]
        if 'hourly' in shaded_data and 'max' in shaded_data['hourly'] and not shaded_data['hourly']['max'].empty:
            plt.plot(shaded_data['hourly']['max'].index, shaded_data['hourly']['max']['temperature'], label=f'Shaded {day}', color='black', linestyle='--', linewidth=1)

        # Add labels, title, and legend
        plt.xlabel('Time')
        plt.ylabel('Max Temperature')
        plt.title(f'Daily Max Temperature - Control vs Shaded ({day})')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)

        # Save the plot
        filename = os.path.join(daily_dir, f'temperature_max_control_vs_shaded_{day}.png')
        print(f"Saving daily max plot to: {filename}")
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()  # Close the plot to free up memory
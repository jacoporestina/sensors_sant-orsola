import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from datetime import datetime

# Load datasets with proper date parsing
def load_data(file_path):
    df = pd.read_csv(file_path, parse_dates=['receivedAt'])
    df['receivedAt'] = pd.to_datetime(df['receivedAt'])
    df.set_index('receivedAt', inplace=True)
    df.index = df.index.tz_localize(None) if df.index.tz is not None else df.index
    return df

# Load datasets
control_daily = load_data('mean_std_data/termoigrometro_control_daily_mean_std.csv')
shaded_daily = load_data('mean_std_data/termoigrometro_shaded_daily_mean_std.csv')
control_hourly = load_data('mean_std_data/termoigrometro_control_hourly_mean_std.csv')
shaded_hourly = load_data('mean_std_data/termoigrometro_shaded_hourly_mean_std.csv')

# Variables to plot
variables = ['temperature', 'humidity', 'vaporPressureDeficit']

def plot_comparison(control_df, shaded_df, variable, start_date, end_date, save_path, time_scale='daily'):
    """Plots mean comparison for a given time period and saves it."""
    # Filter data for the date range
    mask = (control_df.index >= start_date) & (control_df.index <= end_date)
    control_df = control_df.loc[mask]
    shaded_df = shaded_df.loc[mask]

    if control_df.empty or shaded_df.empty:
        print(f"Skipping {variable} for {start_date} to {end_date} (no data)")
        return

    mean_col = f"{variable}_mean_mean"
    std_col = f"{variable}_mean_std"

    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot data
    ax.plot(control_df.index, control_df[mean_col], label='Control', color='black', linestyle="-", linewidth=1)
    ax.fill_between(control_df.index,
                    control_df[mean_col] - 1.96 * control_df[std_col],
                    control_df[mean_col] + 1.96 * control_df[std_col],
                    color='black', alpha=0.2)

    ax.plot(shaded_df.index, shaded_df[mean_col], label='Shaded', color='grey', linestyle="--", linewidth=1)
    ax.fill_between(shaded_df.index,
                    shaded_df[mean_col] - 1.96 * shaded_df[std_col],
                    shaded_df[mean_col] + 1.96 * shaded_df[std_col],
                    color='grey', alpha=0.2)

    # Set titles and labels
    title_date_format = '%Y-%m-%d' if time_scale == 'daily' else '%B %Y'
    ax.set_title(f"{variable.capitalize()} Comparison ({start_date.strftime(title_date_format)}{f' to {end_date.strftime(title_date_format)}' if start_date != end_date else ''})")
    ax.set_ylabel(variable.capitalize())
    ax.legend()

    # X-axis formatting based on time scale
    if time_scale == 'hourly':
        # For hourly data, show hours
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))  # Show every 3 hours to avoid crowding
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.set_xlabel('Time of Day')
    else:
        # For daily data, show days or months depending on time span
        time_span = (end_date - start_date).days
        if time_span <= 31:  # For monthly plots
            ax.xaxis.set_major_locator(mdates.DayLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
            ax.set_xlabel('Day of Month')
        else:
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            ax.set_xlabel('Date')

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    plt.close()
    print(f"Saved plot: {save_path}")

def plot_monthly_comparison():
    """Plots data for each month using daily data."""
    # Create main folders if they don't exist
    os.makedirs("plots/monthly", exist_ok=True)

    # Get all unique year-month combinations
    unique_months = control_daily.index.to_period('M').unique()

    for month_period in unique_months:
        start_date = month_period.start_time
        end_date = month_period.end_time

        # Create variable folders for this month
        for var in variables:
            variable_folder = f"plots/monthly/{var}"
            os.makedirs(variable_folder, exist_ok=True)

            save_path = f"{variable_folder}/{start_date.strftime('%Y-%m')}.png"
            plot_comparison(control_daily, shaded_daily, var, start_date, end_date, save_path, time_scale='daily')

def plot_daily_comparison():
    """Plots data for each day using hourly data."""
    # Create main folders if they don't exist
    os.makedirs("plots/daily", exist_ok=True)

    # Get all unique dates in the hourly data
    unique_dates = pd.to_datetime(control_hourly.index.date).unique()

    for date in unique_dates:
        start_date = pd.to_datetime(date)
        end_date = start_date + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

        # Create variable folders for this day
        for var in variables:
            variable_folder = f"plots/daily/{var}"
            os.makedirs(variable_folder, exist_ok=True)

            save_path = f"{variable_folder}/{start_date.strftime('%Y-%m-%d')}.png"
            plot_comparison(control_hourly, shaded_hourly, var, start_date, end_date, save_path, time_scale='hourly')

# Run both functions
plot_monthly_comparison()
plot_daily_comparison()
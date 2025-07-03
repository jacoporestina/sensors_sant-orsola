import pandas as pd
import matplotlib.pyplot as plt
import os

# Create output folder
output_folder = "plots_rinfrescante_vs_control"
os.makedirs(output_folder, exist_ok=True)

# Load data
rinfrescante_daily = pd.read_csv('hourly_daily_data/termoigrometro_rinfrescante_daily.csv', parse_dates=['receivedAt'])
control_daily = pd.read_csv('mean_std_data/termoigrometro_control_daily_mean_std.csv', parse_dates=['receivedAt'])
rinfrescante_hourly = pd.read_csv('hourly_daily_data/termoigrometro_rinfrescante_hourly.csv', parse_dates=['receivedAt'])
control_hourly = pd.read_csv('mean_std_data/termoigrometro_control_hourly_mean_std.csv', parse_dates=['receivedAt'])

# --- DAILY: Plot temperature for each month ---
rinfrescante_daily['month'] = rinfrescante_daily['receivedAt'].dt.to_period('M')
control_daily['month'] = control_daily['receivedAt'].dt.to_period('M')

months = sorted(set(rinfrescante_daily['month'].dropna()) | set(control_daily['month'].dropna()))
for month in months:
    rinfrescante_month = rinfrescante_daily[rinfrescante_daily['month'] == month]
    control_month = control_daily[control_daily['month'] == month]
    # Skip if rinfrescante data is empty or all temperature_mean is NaN
    if rinfrescante_month.empty or rinfrescante_month['temperature_mean'].dropna().empty:
        continue
    plt.figure(figsize=(10, 5))
    plt.plot(rinfrescante_month['receivedAt'], rinfrescante_month['temperature_mean'], label='Rinfrescante')
    plt.plot(control_month['receivedAt'], control_month['temperature_mean_mean'], label='Control')
    plt.xlabel('Day')
    plt.ylabel('Temperature (°C)')
    plt.title(f'Daily Temperature - {month}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    # Set x-axis ticks to every day
    plt.xticks(rinfrescante_month['receivedAt'].dt.normalize().unique(),
               rinfrescante_month['receivedAt'].dt.strftime('%Y-%m-%d').unique(), rotation=45)
    plt.savefig(os.path.join(output_folder, f'daily_temperature_{month}.png'))
    plt.close()

# --- HOURLY: Plot temperature for each day ---
rinfrescante_hourly['date'] = rinfrescante_hourly['receivedAt'].dt.date
control_hourly['date'] = control_hourly['receivedAt'].dt.date

days = sorted(set(rinfrescante_hourly['date'].dropna()) | set(control_hourly['date'].dropna()))
for day in days:
    rinfrescante_day = rinfrescante_hourly[rinfrescante_hourly['date'] == day]
    control_day = control_hourly[control_hourly['date'] == day]
    # Skip if rinfrescante data is empty or all temperature_mean is NaN
    if rinfrescante_day.empty or rinfrescante_day['temperature_mean'].dropna().empty:
        continue
    plt.figure(figsize=(10, 5))
    plt.plot(rinfrescante_day['receivedAt'].dt.hour, rinfrescante_day['temperature_mean'], label='Rinfrescante')
    plt.plot(control_day['receivedAt'].dt.hour, control_day['temperature_mean_mean'], label='Control')
    plt.xlabel('Hour')
    plt.ylabel('Temperature (°C)')
    plt.title(f'Hourly Temperature - {day}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    # Set x-axis ticks to every hour present in rinfrescante data
    plt.xticks(rinfrescante_day['receivedAt'].dt.hour.unique())
    plt.savefig(os.path.join(output_folder, f'hourly_temperature_{day}.png'))
    plt.close()
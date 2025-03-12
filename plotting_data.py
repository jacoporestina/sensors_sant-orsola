import pandas as pd
import matplotlib.pyplot as plt
import os

# Define CSV file paths
csv_files = [
    "data/PAR fragola non ombreggiata 982_2024-07-01_2025-03-06.csv",
    "data/PAR fragola ombreggiata 981_2024-07-01_2025-03-06.csv",
    "data/Termoigrometro 6 fragola ombreggiata 976_2024-07-01_2025-03-06.csv",
    "data/Termoigrometro fragola non ombreggiata 1027_2024-07-01_2025-03-06.csv",
]

# Define variable names and corresponding folders + colors
VARIABLES = {
    'photosyntheticallyActiveRadiation': ('PAR', 'goldenrod'),
    'temperature': ('Temperature', 'red'),
    'humidity': ('Humidity', 'blue'),
    'vaporPressureDeficit': ('VPD', 'green'),
}

# Define the range of months from July to March
MONTH_RANGE = [f"2024-{str(m).zfill(2)}" for m in range(7, 13)] + [f"2025-{str(m).zfill(2)}" for m in range(1, 4)]

def create_folder(variable, avg_type):
    """Creates a subfolder for each variable and averaging type (Hourly/Daily)."""
    folder_path = os.path.join("plots", variable, avg_type)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def load_data(file):
    """Loads CSV data, converts 'receivedAt' to datetime, and calculates both hourly and daily averages."""
    if not os.path.exists(file):
        print(f"❌ File not found: {file}")
        return None, None

    df = pd.read_csv(file, delimiter=';')

    if 'receivedAt' not in df.columns:
        print(f"❌ Missing 'receivedAt' column in {file}")
        return None, None

    df['receivedAt'] = pd.to_datetime(df['receivedAt'], errors='coerce')
    df.dropna(subset=['receivedAt'], inplace=True)  # Remove invalid timestamps

    # Extract month, hour, and date for grouping
    df['Month'] = df['receivedAt'].dt.strftime('%Y-%m')
    df['Hour'] = df['receivedAt'].dt.floor('H')  # Round timestamps to the nearest hour
    df['Date'] = df['receivedAt'].dt.date  # Extract only the date

    # Calculate hourly and daily averages
    df_hourly = df.groupby(['Month', 'Hour']).mean(numeric_only=True).reset_index()
    df_daily = df.groupby(['Month', 'Date']).mean(numeric_only=True).reset_index()

    return df_hourly, df_daily

def plot_variable(df, column, file_name, month, avg_type):
    """Plots either hourly or daily averaged data for a given month."""
    if column not in df.columns:
        return

    df_month = df[df['Month'] == month]
    if df_month.empty:
        return

    # Determine the correct folder & color
    variable_name, color = VARIABLES.get(column, ('Unknown', 'black'))
    folder_path = create_folder(variable_name, avg_type)

    plt.figure(figsize=(10, 6))

    x_axis = 'Hour' if avg_type == "Hourly" else 'Date'
    plt.plot(df_month[x_axis], df_month[column], label=f'{avg_type} Avg {column}', color=color)

    plt.xlabel(f'Time ({avg_type})')
    plt.ylabel(column)
    plt.title(f'{avg_type} Average {column} in {month} - {file_name}')

    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Save the plot
    plot_path = os.path.join(folder_path, f"{file_name}_{column}_{avg_type}Avg_{month}.png")
    plt.savefig(plot_path, dpi=300)
    plt.close()

    print(f"✅ Plot saved: {plot_path}")

def process_file(file):
    """Processes a single file: loads data, computes averages, and generates plots."""
    df_hourly, df_daily = load_data(file)
    if df_hourly is None or df_daily is None:
        return

    file_name = os.path.basename(file).replace('.csv', '')

    # Generate hourly and daily plots for each month
    for month in MONTH_RANGE:
        for column in VARIABLES:
            plot_variable(df_hourly, column, file_name, month, "Hourly")
            plot_variable(df_daily, column, file_name, month, "Daily")

# Process all files
for file in csv_files:
    process_file(file)

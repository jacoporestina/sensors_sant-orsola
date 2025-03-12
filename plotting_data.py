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

# Create a folder for plots
PLOT_FOLDER = "plots"
os.makedirs(PLOT_FOLDER, exist_ok=True)

# Columns to be plotted separately
SEPARATE_PLOTS = {'temperature', 'humidity', 'vaporPressureDeficit', 'photosyntheticallyActiveRadiation'}

def load_data(file):
    """Loads CSV data, converts 'receivedAt' to datetime, and handles errors."""
    if not os.path.exists(file):
        print(f"❌ File not found: {file}")
        return None

    df = pd.read_csv(file, delimiter=';')

    if 'receivedAt' not in df.columns:
        print(f"❌ Missing 'receivedAt' column in {file}")
        return None

    df['receivedAt'] = pd.to_datetime(df['receivedAt'], errors='coerce')
    df.dropna(subset=['receivedAt'], inplace=True)  # Remove invalid timestamps

    return df

def plot_variable(df, column, file_name):
    """Plots a single variable over time and saves the figure."""
    if column not in df.columns:
        return

    plt.figure(figsize=(10, 6))
    plt.plot(df['receivedAt'], df[column], label=column, color='b')

    plt.xlabel('Time')
    plt.ylabel(column)
    plt.title(f'{column} Over Time - {file_name}')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Save the plot
    plot_path = os.path.join(PLOT_FOLDER, f"{file_name}_{column}.png")
    plt.savefig(plot_path, dpi=300)
    plt.close()

    print(f"✅ Plot saved: {plot_path}")

def process_file(file):
    """Processes a single file: loads data and generates plots."""
    df = load_data(file)
    if df is None:
        return

    file_name = os.path.basename(file).replace('.csv', '')

    # Plot each selected variable separately
    for column in SEPARATE_PLOTS:
        plot_variable(df, column, file_name)

# Process all files
for file in csv_files:
    process_file(file)

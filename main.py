from file_processing import load_data
from plotting_part import plot_variables

# Define CSV file paths for control (non-shaded) and shaded conditions
csv_files = {
    "photosyntheticallyActiveRadiation": {
        "control": "data/PAR fragola non ombreggiata 982_2024-07-01_2025-03-06.csv",
        "shaded": "data/PAR fragola ombreggiata 981_2024-07-01_2025-03-06.csv",
    },
    "temperature": {
        "control": "data/Termoigrometro fragola non ombreggiata 1027_2024-07-01_2025-03-06.csv",
        "shaded": "data/Termoigrometro 6 fragola ombreggiata 976_2024-07-01_2025-03-06.csv",
    },
    "humidity": {
        "control": "data/Termoigrometro fragola non ombreggiata 1027_2024-07-01_2025-03-06.csv",
        "shaded": "data/Termoigrometro 6 fragola ombreggiata 976_2024-07-01_2025-03-06.csv",
    },
    "vaporPressureDeficit": {
        "control": "data/Termoigrometro fragola non ombreggiata 1027_2024-07-01_2025-03-06.csv",
        "shaded": "data/Termoigrometro 6 fragola ombreggiata 976_2024-07-01_2025-03-06.csv",
    },
}


# Load data and get the means
means_data = load_data(csv_files)
print(means_data)

# Plot the data
plot_variables(means_data, save_dir='plots')


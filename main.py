from file_processing import load_data

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


import matplotlib.pyplot as plt
import pandas as pd

# Access temperature data
t_shaded_hourly = means_data['temperature']['shaded']['hourly']
t_control_hourly = means_data['temperature']['control']['hourly']
# Access PAR data
par_shaded_hourly = means_data['photosyntheticallyActiveRadiation']['shaded']['hourly']
par_control_hourly = means_data['photosyntheticallyActiveRadiation']['control']['hourly']

print(t_shaded_hourly.head())
print(t_control_hourly.head())
print(par_shaded_hourly.head())
print(par_control_hourly.head())

# create the plot
plt.figure(figsize=(12, 6))

# plot temperature data
plt.plot(t_shaded_hourly.index, t_shaded_hourly['temperature'], label='Shaded temperature', color='blue')
plt.ylabel('Temperature (°C)')
plt.title('Hourly Temperature in Shaded conditions')
plt.legend()
plt.show()

plt.savefig('temperature_shaded.png', dpi=300, bbox_inches='tight')
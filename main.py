from file_processing import load_data
from data_to_csv import transform_csv
from means_calculation import calculate_means
from plot_data import plot_variables
from plot_comparison import plot_shaded_vs_control
from plot_max_t import plot_max_temperature
import pandas as pd


# Define CSV file paths for control (non-shaded) and shaded conditions
csv_files = {
    "photosyntheticallyActiveRadiation": {
        "control": {
            "repetition_1" : "data/PAR fragola non ombreggiata 982_2024-07-01_2025-03-06.csv",
        },
        "shaded": {
            "repetition_1" : "data/PAR fragola ombreggiata 981_2024-07-01_2025-03-06.csv",
        },
    },
    "temperature": {
        "control": {
            "repetition_1" : "data/Termoigrometro controllo rep_1.csv",
            "repetition_2" : "data/Termoigrometro controllo rep_2.csv",
            "repetition_3" : "data/Termoigrometro controllo rep_3.csv",
        },
        "shaded": {
            "repetition_1" : "data/Termoigrometro ombreggiata rep_1.csv",
            "repetition_2" : "data/Termoigrometro ombreggiata rep_2.csv",
            "repetition_3" : "data/Termoigrometro ombreggiata rep_3.csv",
        },
    },
    "humidity": {
        "control": {
            "repetition_1" : "data/Termoigrometro controllo rep_1.csv",
            "repetition_2" : "data/Termoigrometro controllo rep_2.csv",
            "repetition_3" : "data/Termoigrometro controllo rep_3.csv",
        },
        "shaded": {
            "repetition_1" : "data/Termoigrometro ombreggiata rep_1.csv",
            "repetition_2" : "data/Termoigrometro ombreggiata rep_2.csv",
            "repetition_3" : "data/Termoigrometro ombreggiata rep_3.csv",
        },
    },
    "vaporPressureDeficit": {
        "control": {
            "repetition_1" : "data/Termoigrometro controllo rep_1.csv",
            "repetition_2" : "data/Termoigrometro controllo rep_2.csv",
            "repetition_3" : "data/Termoigrometro controllo rep_3.csv",
        },
        "shaded": {
            "repetition_1" : "data/Termoigrometro ombreggiata rep_1.csv",
            "repetition_2" : "data/Termoigrometro ombreggiata rep_2.csv",
            "repetition_3" : "data/Termoigrometro ombreggiata rep_3.csv",
        },
    },
}


# Load data and get the means
dictionary_data = load_data(csv_files)
#print(dictionary_data['photosyntheticallyActiveRadiation']['control']['repetition_1']['day']['2024-08-15']['hourly'])
#print(dictionary_data['temperature']['control']['repetition_2']['month']['2024-07'])

# Calculate means across repetions in dictionary_data
#means_data = calculate_means(dictionary_data)
#print(means_data['temperature']['control']['month']['2024-07'])
#print(means_data['photosyntheticallyActiveRadiation']['shaded']['day']['2024-08-15'])

# Flatten the dictionary
dictionary_data_to_csv = transform_csv(dictionary_data)

# Convert to a DataFrame
df = pd.DataFrame(dictionary_data_to_csv)

# Save to CSV
df.to_csv("dictionary_data.csv", index=False)
print("dictionary_data_to_csv has been exported to dictionary_data.csv")



# Plot the data
#plot_variables(means_data, save_dir='plots')

# Plot the comparisons between treatments
#plot_shaded_vs_control(means_data, save_dir='plots/shaded_vs_control')

# Plot comparisons between treatments of max temperatures
#plot_max_temperature(means_data, save_dir='plots/max_temperature')
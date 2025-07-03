from file_processing import process_files, compute_mean_stdev, combine_par_and_termoigrometro

"""Main file to handle all the functions for file processing and plots."""



# Specify file path of the raw data
csv_files = [
    "data/termoigrometro_control_1.csv",
    "data/termoigrometro_control_2.csv",
    "data/termoigrometro_control_3.csv",
    "data/termoigrometro_shaded_1.csv",
    "data/termoigrometro_shaded_2.csv",
    "data/termoigrometro_shaded_3.csv",
    "data/PAR_control.csv",
    "data/PAR_shaded.csv",
    "data/termoigrometro_rinfrescante.csv",
]

# Specify file path of data elaborated for means, max and min.
termoigrometro_control_daily = [
    "hourly_daily_data/termoigrometro_control_1_daily.csv",
    "hourly_daily_data/termoigrometro_control_2_daily.csv",
    "hourly_daily_data/termoigrometro_control_3_daily.csv",
]

termoigrometro_control_hourly = [
    "hourly_daily_data/termoigrometro_control_1_hourly.csv",
    "hourly_daily_data/termoigrometro_control_2_hourly.csv",
    "hourly_daily_data/termoigrometro_control_3_hourly.csv",
]

termoigrometro_shaded_daily = [
    "hourly_daily_data/termoigrometro_shaded_1_daily.csv",
    "hourly_daily_data/termoigrometro_shaded_2_daily.csv",
    "hourly_daily_data/termoigrometro_shaded_3_daily.csv",
]

termoigrometro_shaded_hourly = [
    "hourly_daily_data/termoigrometro_shaded_1_hourly.csv",
    "hourly_daily_data/termoigrometro_shaded_2_hourly.csv",
    "hourly_daily_data/termoigrometro_shaded_3_hourly.csv",
]

termoigrometro_rinfrescante = [
    "hourly_daily_data/termoigrometro_rinfrescante_daily.csv",
    "hourly_daily_data/termoigrometro_rinfrescante_hourly.csv",
]

# Compute hourly and daily means, max and min
process_files(csv_files)

# Compute and save statistics (mean and std)
compute_mean_stdev(termoigrometro_control_daily, "termoigrometro_control_daily")
compute_mean_stdev(termoigrometro_control_hourly, "termoigrometro_control_hourly")
compute_mean_stdev(termoigrometro_shaded_daily, "termoigrometro_shaded_daily")
compute_mean_stdev(termoigrometro_shaded_hourly, "termoigrometro_shaded_hourly")
compute_mean_stdev(termoigrometro_rinfrescante, "termoigrometro_rinfrescante")

# combine the PAR files with the termoigrometro data
combine_par_and_termoigrometro() # Before using the function, copy paste PAR files into mean_std_data folder.
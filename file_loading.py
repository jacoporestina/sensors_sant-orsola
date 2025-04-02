import pandas as pd
import os
import glob

'''
csv_files = [
    "data/termoigrometro_control_1.csv",
    "data/termoigrometro_control_2.csv",
    "data/termoigrometro_control_3.csv",
    "data/termoigrometro_shaded_1.csv",
    "data/termoigrometro_shaded_2.csv",
    "data/termoigrometro_shaded_3.csv",
    "data/PAR_control.csv",
    "data/PAR_shaded.csv",
]

# Ensure the output directory exists
save_path = "hourly_daily_data"
os.makedirs(save_path, exist_ok=True)

for file in csv_files:
    df = pd.read_csv(file, sep=';')

    # Drop unnecessary columns
    columns_to_drop = ['batteryValue', 'batteryLevel', 'device', 'providerDeviceId']
    df.drop(columns_to_drop, axis=1, inplace=True)

    # Transform receivedAt to date
    df['receivedAt'] = pd.to_datetime(df['receivedAt'])
    df.set_index('receivedAt', inplace=True)

    # Calculate means, max and min for every hour and day
    df_hourly_means = df.resample('H').mean()
    df_daily_means = df.resample('D').mean()
    df_hourly_max = df.resample('H').max()
    df_daily_max = df.resample('D').max()
    df_hourly_min = df.resample('H').min()
    df_daily_min = df.resample('D').min()

    # Combine dfs with the same resampling type
    df_hourly = pd.concat([df_hourly_means, df_hourly_max, df_hourly_min], axis=1, keys=['mean', 'max', 'min'])
    df_daily = pd.concat([df_daily_means, df_daily_max, df_daily_min], axis=1, keys=['mean', 'max', 'min'])
    print(df_hourly.head())

    # Flatten the multi-index columns and rename them
    df_hourly.columns = [f"{level1}_{level0}" if level0 != 'receivedAt' else level0
                    for level0, level1 in df_hourly.columns]
    df_daily.columns = [f"{level1}_{level0}" if level0 != 'receivedAt' else level0
                   for level0, level1 in df_daily.columns]

    # Reset index to make 'receivedAt' a column again
    df_hourly = df_hourly.reset_index()
    df_daily = df_daily.reset_index()

    # Extract the filename and save the CSVs
    filename = os.path.basename(file).replace(".csv", "")
    df_hourly.to_csv(f"{save_path}/{filename}_hourly.csv")
    df_daily.to_csv(f"{save_path}/{filename}_daily.csv")
    print("data successfully converted into cvs files.")
'''

# make sure the folder to save files exist
save_path_2 = "mean_stdev_data"
os.makedirs(save_path_2, exist_ok=True)

files = [
    "hourly_daily_data/termoigrometro_control_1_hourly.csv",
    "hourly_daily_data/termoigrometro_control_2_hourly.csv",
    "hourly_daily_data/termoigrometro_control_3_hourly.csv",
]

# Loop through the files
dfs = [pd.read_csv(f) for f in files]
print(dfs[0].columns)
print(dfs[0].head())

# concatenate all dataframes
dfs_all = pd.concat(dfs)

# Compute mean and standard
df_summary = dfs_all.groupby("receivedAt").agg("mean", "stdev")
print(df_summary.head())

# save file
summary_file = os.path.join(save_path_2, "hourly_mean_std.csv")
df_summary.to_csv(summary_file)

# Print confirmation
print("Mean and standard deviation computed and saved as:", summary_file)

import pandas as pd
import os

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

    # Extract the filename and save the CSVs
    filename = os.path.basename(file).replace(".csv", "")
    df_hourly.to_csv(f"{save_path}/{filename}_hourly.csv")
    df_daily.to_csv(f"{save_path}/{filename}_daily.csv")
    print("data successfully converted into cvs files.")



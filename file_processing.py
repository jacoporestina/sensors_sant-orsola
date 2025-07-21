import pandas as pd
import os


def process_files(csv_files):
    """method to calculate means, max and min of data."""
    for file in csv_files:
        df = pd.read_csv(file, sep=';')

        # Drop unnecessary columns
        columns_to_drop = ['batteryValue', 'batteryLevel', 'device', 'providerDeviceId']
        df.drop(columns_to_drop, axis=1, inplace=True)

        # Transform receivedAt to date
        df['receivedAt'] = pd.to_datetime(df['receivedAt'])
        df.set_index('receivedAt', inplace=True)

        # Calculate means, max and min for every hour
        df_hourly_mean = df.resample('H').mean()

        # Calculate means, max and min for every day
        df_daily_mean = df_hourly_mean.resample('D').mean()
        df_daily_max = df_hourly_mean.resample('D').max()
        df_daily_min = df_hourly_mean.resample('D').min()

        # Claculate means, max and min for every month
        df_monthly_mean = df_daily_mean.resample('M').mean()
        df_monthly_max = df_daily_max.resample('M').mean()
        df_monthly_min = df_daily_min.resample('M').mean()

        # Combine dfs with the same resampling type
        df_hourly = pd.concat([df_hourly_mean], axis=1, keys=['mean'])
        df_daily = pd.concat([df_daily_mean, df_daily_max, df_daily_min], axis=1, keys=['mean', 'max', 'min'])
        df_monthly = pd.concat([df_monthly_mean, df_monthly_max, df_monthly_min], axis=1, keys=['mean', 'max', 'min'])
        print(df_hourly.head())

        # Flatten the multi-index columns and rename them
        df_hourly.columns = [f"{level1}_{level0}" if level0 != 'receivedAt' else level0
                        for level0, level1 in df_hourly.columns]
        df_daily.columns = [f"{level1}_{level0}" if level0 != 'receivedAt' else level0
                    for level0, level1 in df_daily.columns]
        df_monthly.columns = [f"{level1}_{level0}" if level0 != 'receivedAt' else level0
                    for level0, level1 in df_monthly.columns]


        # Add DLI column
        if 'photosyntheticallyActiveRadiation_mean' in df_hourly.columns:
            df_daily['DLI_mol m-2 d-1'] = df_hourly['photosyntheticallyActiveRadiation_mean'].resample('D').sum() * 3600 / 1000000
        else:
            print(f"Column ['photosyntheticallyActiveRadiation_mean'] missing in {file}.")


        # Calculate mean temperatures for nighttime and daytime
        df_hourly['hour'] = df_hourly.index.hour
        df_hourly['is_daytime'] = df_hourly['hour'].apply(lambda x: 1 if 6 <= x < 20 else 0)

        if 'temperature_mean' in df_hourly.columns:
            df_daily['temperature_daytime_mean'] = df_hourly[df_hourly['is_daytime'] == 1].resample('D')['temperature_mean'].mean()
            df_daily['temperature_nighttime_mean'] = df_hourly[df_hourly['is_daytime'] == 0].resample('D')['temperature_mean'].mean()
            df_monthly['temperature_daytime_mean'] = df_daily['temperature_daytime_mean'].resample('M').mean()
            df_monthly['temperature_nighttime_mean'] = df_daily['temperature_nighttime_mean'].resample('M').mean()
        else:
            print(f"Column ['temperature_mean'] missing in {file}.")

        # Drop temporary columns
        df_hourly.drop(['hour', 'is_daytime'], axis=1, inplace=True)

        # Reset index to make 'receivedAt' a column again
        df_hourly = df_hourly.reset_index()
        df_daily = df_daily.reset_index()

        # Ensure the output directory exists
        save_path = "hourly_daily_data"
        os.makedirs(save_path, exist_ok=True)

        # Extract the filename and save the CSVs
        filename = os.path.basename(file).replace(".csv", "")
        df_hourly.to_csv(f"{save_path}/{filename}_hourly.csv")
        df_daily.to_csv(f"{save_path}/{filename}_daily.csv")
        df_monthly.to_csv(f"{save_path}/{filename}_monthly.csv")
        print("data successfully converted into cvs files.")



def compute_mean_stdev(file_list, group_name):
    """Compute mean and standard deviation across files and save the output."""
    if not file_list:  # Skip if no files found
        print(f"No files found for {group_name}")
        return

    # Read files
    dfs = [pd.read_csv(f) for f in file_list]

    # Concatenate all dataframes
    dfs_all = pd.concat(dfs)

    # Compute mean and standard deviation
    df_summary = dfs_all.groupby("receivedAt").agg(["mean", "std"])

    # Rename columns
    df_summary.columns = [f"{col}_{stat}" for col, stat in df_summary.columns]

    # Save file
    save_path = "mean_std_data"
    os.makedirs(save_path, exist_ok=True)
    summary_file = os.path.join(save_path, f"{group_name}_mean_std.csv")
    df_summary.to_csv(summary_file)

    print(f"Saved {group_name} summary to {summary_file}")



def combine_par_and_termoigrometro(mean_std_folder="mean_std_data"):
    """Combine PAR data with termoigrometro data."""
    # List all files in the mean_std_data folder
    files = [f for f in os.listdir(mean_std_folder) if f.endswith(".csv")]

    # Explicit mapping of PAR files to termoigrometro files
    file_mapping = {
        "PAR_control_daily": "termoigrometro_control_daily_mean_std.csv",
        "PAR_control_hourly": "termoigrometro_control_hourly_mean_std.csv",
        "PAR_shaded_daily": "termoigrometro_shaded_daily_mean_std.csv",
        "PAR_shaded_hourly": "termoigrometro_shaded_hourly_mean_std.csv",
    }

    for par_file_key, termo_file_name in file_mapping.items():
        # Find the PAR file
        par_file = next((f for f in files if par_file_key in f), None)
        if not par_file:
            print(f"No PAR file found for key {par_file_key}")
            continue

        # Find the corresponding termoigrometro file
        termo_file = next((f for f in files if termo_file_name in f), None)
        if not termo_file:
            print(f"No matching termoigrometro file found for {par_file_key}")
            continue

        # Load the PAR and termoigrometro data
        par_df = pd.read_csv(os.path.join(mean_std_folder, par_file))
        termo_df = pd.read_csv(os.path.join(mean_std_folder, termo_file))

        # Rename the column if it exists
        if 'photosyntheticallyActiveRadiation_mean' in par_df.columns:
            par_df.rename(columns={'photosyntheticallyActiveRadiation_mean': 'photosyntheticallyActiveRadiation_mean_mean'}, inplace=True)

        # Determine columns to merge dynamically
        merge_columns = ['receivedAt']
        if 'photosyntheticallyActiveRadiation_mean_mean' in par_df.columns:
            merge_columns.append('photosyntheticallyActiveRadiation_mean_mean')
        if 'DLI_mol m-2 d-1' in par_df.columns:
            merge_columns.append('DLI_mol m-2 d-1')

        # Merge the data on the 'receivedAt' column
        combined_df = pd.merge(termo_df, par_df[merge_columns], on='receivedAt', how='left')

        # Save the combined file
        combined_file = os.path.join(mean_std_folder, f"combined_termoigrometro_{par_file_key}_mean_std.csv")
        combined_df.to_csv(combined_file, index=False)
        print(f"Combined file saved to {combined_file}")
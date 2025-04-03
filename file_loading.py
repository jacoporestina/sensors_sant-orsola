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

        # Ensure the output directory exists
        save_path = "hourly_daily_data"
        os.makedirs(save_path, exist_ok=True)

        # Extract the filename and save the CSVs
        filename = os.path.basename(file).replace(".csv", "")
        df_hourly.to_csv(f"{save_path}/{filename}_hourly.csv")
        df_daily.to_csv(f"{save_path}/{filename}_daily.csv")
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

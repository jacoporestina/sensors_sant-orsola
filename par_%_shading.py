import pandas as pd

# Load the control and shaded datasets
control_df_daily = pd.read_csv('hourly_daily_data/PAR_control_daily.csv', usecols=['receivedAt', 'photosyntheticallyActiveRadiation_mean', 'DLI_mol m-2 d-1'])
shaded_df_daily = pd.read_csv('hourly_daily_data/PAR_shaded_daily.csv', usecols=['receivedAt', 'photosyntheticallyActiveRadiation_mean', 'DLI_mol m-2 d-1'])
control_df_hourly = pd.read_csv('hourly_daily_data/PAR_control_hourly.csv', usecols=['receivedAt', 'photosyntheticallyActiveRadiation_mean'])
shaded_df_hourly = pd.read_csv('hourly_daily_data/PAR_shaded_hourly.csv', usecols=['receivedAt', 'photosyntheticallyActiveRadiation_mean'])


# Rename the PAR columns for clarity before merging
control_df_daily.rename(columns={'photosyntheticallyActiveRadiation_mean': 'PAR_control'}, inplace=True)
shaded_df_daily.rename(columns={'photosyntheticallyActiveRadiation_mean': 'PAR_shaded'}, inplace=True)
control_df_daily.rename(columns={'DLI_mol m-2 d-1': 'DLI_control'}, inplace=True)
shaded_df_daily.rename(columns={'DLI_mol m-2 d-1': 'DLI_shaded'}, inplace=True)
control_df_hourly.rename(columns={'photosyntheticallyActiveRadiation_mean': 'PAR_control_hourly'}, inplace=True)
shaded_df_hourly.rename(columns={'photosyntheticallyActiveRadiation_mean': 'PAR_shaded_hourly'}, inplace=True)

# Merge the two DataFrames on receivedAt
merged_df_daily = pd.merge(control_df_daily, shaded_df_daily, on='receivedAt')
merged_df_hourly = pd.merge(control_df_hourly, shaded_df_hourly, on='receivedAt')

# Calculate percentage difference
merged_df_daily['PAR_percent_diff'] = ((merged_df_daily['PAR_control'] - merged_df_daily['PAR_shaded']) / merged_df_daily['PAR_control']) * 100
merged_df_daily['DLI_percent_diff'] = ((merged_df_daily['DLI_control'] - merged_df_daily['DLI_shaded']) / merged_df_daily['DLI_control']) * 100
merged_df_hourly['PAR_percent_diff'] = ((merged_df_hourly['PAR_control_hourly'] - merged_df_hourly['PAR_shaded_hourly']) / merged_df_hourly['PAR_control_hourly']) * 100

# Calculate average percentage differences
avg_PAR_percent_diff = merged_df_daily['PAR_percent_diff'].mean()
avg_DLI_percent_diff = merged_df_daily['DLI_percent_diff'].mean()
avg_PAR_hourly_percent_diff = merged_df_hourly['PAR_percent_diff'].mean()

# Print the averages
print(f"Average PAR Percent Difference: {avg_PAR_percent_diff:.2f}%")
print(f"Average DLI Percent Difference: {avg_DLI_percent_diff:.2f}%")
print(f"Average Hourly PAR Percent Difference: {avg_PAR_hourly_percent_diff:.2f}%")

# Save to CSV
merged_df_daily.to_csv('PAR_comparison_daily.csv', index=False)
merged_df_hourly.to_csv('PAR_comparison_hourly.csv', index=False)

print("Output saved to PAR_comparison_daily.csv")

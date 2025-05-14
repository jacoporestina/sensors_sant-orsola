import pandas as pd

# Load the control and shaded datasets
control_df = pd.read_csv('hourly_daily_data/PAR_control_daily.csv', usecols=['receivedAt', 'photosyntheticallyActiveRadiation_mean', 'DLI_mol m-2 d-1'])
shaded_df = pd.read_csv('hourly_daily_data/PAR_shaded_daily.csv', usecols=['receivedAt', 'photosyntheticallyActiveRadiation_mean', 'DLI_mol m-2 d-1'])

# Rename the PAR columns for clarity before merging
control_df.rename(columns={'photosyntheticallyActiveRadiation_mean': 'PAR_control'}, inplace=True)
shaded_df.rename(columns={'photosyntheticallyActiveRadiation_mean': 'PAR_shaded'}, inplace=True)
control_df.rename(columns={'DLI_mol m-2 d-1': 'DLI_control'}, inplace=True)
shaded_df.rename(columns={'DLI_mol m-2 d-1': 'DLI_shaded'}, inplace=True)

# Merge the two DataFrames on receivedAt
merged_df = pd.merge(control_df, shaded_df, on='receivedAt')

# Calculate percentage difference
merged_df['PAR_percent_diff'] = ((merged_df['PAR_control'] - merged_df['PAR_shaded']) / merged_df['PAR_control']) * 100
merged_df['DLI_percent_diff'] = ((merged_df['DLI_control'] - merged_df['DLI_shaded']) / merged_df['DLI_control']) * 100

# Calculate average percentage differences
avg_PAR_percent_diff = merged_df['PAR_percent_diff'].mean()
avg_DLI_percent_diff = merged_df['DLI_percent_diff'].mean()

# Print the averages
print(f"Average PAR Percent Difference: {avg_PAR_percent_diff:.2f}%")
print(f"Average DLI Percent Difference: {avg_DLI_percent_diff:.2f}%")

# Save to CSV
merged_df.to_csv('PAR_comparison_daily.csv', index=False)

print("Output saved to PAR_comparison_daily.csv")

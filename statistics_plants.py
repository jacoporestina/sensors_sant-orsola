import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load the data
data_path = "data/plant_physiology.csv"
output_dir = "statistics_output/"
os.makedirs(output_dir, exist_ok=True)

df = pd.read_csv(data_path)

# Group data by variable
for variable, label in [
    ('crown no.', 'Crown Number'), ('inflorescence no.', 'Inflorescence Number'),
    ('flower no.', 'Flower Number'), ('fruit no.', 'Fruit Number'),
    ('leaf no.', 'Leaf Number'), ('petiole length mean (cm)', 'Petiole Length'),
]:
    variable_output_dir = os.path.join(output_dir, variable.replace(' ', '_'))
    os.makedirs(variable_output_dir, exist_ok=True)

    # Open a single text file for the variable
    with open(os.path.join(variable_output_dir, f"{variable}_anova_results.txt"), "w") as summary_file:
        summary_file.write(f"ANOVA Results and Assumption Tests for {label}:\n\n")

        for date in df['date'].unique():
            sanitized_date = date.replace("/", "-")  # Replace slashes with hyphens
            date_data = df[df['date'] == date]

            # Perform ANOVA
            anova_result = stats.f_oneway(
                date_data[date_data['treatment'] == 'control'][variable],
                date_data[date_data['treatment'] == 'shaded'][variable]
            )

            # Test assumptions
            shapiro_control = stats.shapiro(date_data[date_data['treatment'] == 'control'][variable])
            shapiro_shaded = stats.shapiro(date_data[date_data['treatment'] == 'shaded'][variable])
            levene_test = stats.levene(
                date_data[date_data['treatment'] == 'control'][variable],
                date_data[date_data['treatment'] == 'shaded'][variable]
            )

            # Append results to the summary file
            summary_file.write(f"Date: {date}\n")
            summary_file.write(f"F-statistic: {anova_result.statistic}, p-value: {anova_result.pvalue}\n")
            summary_file.write(f"Shapiro-Wilk Test (Control): W={shapiro_control.statistic}, p={shapiro_control.pvalue}\n")
            summary_file.write(f"Shapiro-Wilk Test (Shaded): W={shapiro_shaded.statistic}, p={shapiro_shaded.pvalue}\n")
            summary_file.write(f"Levene's Test: W={levene_test.statistic}, p={levene_test.pvalue}\n\n")

            # Generate QQ plot for the date
            plt.figure()
            stats.probplot(date_data[variable], dist="norm", plot=plt)
            plt.title(f"QQ Plot for {label} on {date}")
            plt.savefig(os.path.join(variable_output_dir, f"{sanitized_date}_qq_plot.png"))
            plt.close()

# Ensure date is parsed and sorted
df['date'] = pd.to_datetime(df['date'], dayfirst=True)  # Adjust date format if needed
df = df.sort_values('date')
df['date_str'] = df['date'].dt.strftime('%Y-%m-%d')

# Unique measurement dates (as categories)
date_labels = sorted(df['date_str'].unique())

# Plot styles
marker_styles = {'control': 'o', 'shaded': 's'}
line_color = 'black'

# Output directory
plot_output_dir = "statistics_output/line_plots"
os.makedirs(plot_output_dir, exist_ok=True)

# Variables to plot
variables = [
    ('crown no.', 'Crown Number'),
    ('inflorescence no.', 'Inflorescence Number'),
    ('flower no.', 'Flower Number'),
    ('fruit no.', 'Fruit Number'),
    ('leaf no.', 'Leaf Number'),
    ('petiole length mean (cm)', 'Petiole Length'),
]

# Plot each variable
for variable, label in variables:
    plt.figure(figsize=(6, 4))

    for treatment in df['treatment'].unique():
        sub_df = df[df['treatment'] == treatment]

        # Group and aggregate by string-formatted date
        grouped = sub_df.groupby('date_str').agg(
            mean=(variable, 'mean'),
            std=(variable, 'std')
        ).reindex(date_labels).reset_index()

        plt.errorbar(
            grouped['date_str'], grouped['mean'], yerr=grouped['std'],
            fmt=marker_styles[treatment] + '-', color=line_color,
            label=treatment.capitalize(), capsize=4,
            elinewidth=1, linewidth=1.5, markersize=6
        )

    plt.xlabel('Date')
    plt.ylabel(label)
    plt.title(label)
    plt.xticks(date_labels, rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(plot_output_dir, f"{variable.replace(' ', '_')}_lineplot.png"))
    plt.close()


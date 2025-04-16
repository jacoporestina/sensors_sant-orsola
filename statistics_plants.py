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

# Group data by date
dates = df['date'].unique()

for date in dates:
    sanitized_date = date.replace("/", "-")  # Replace slashes with hyphens
    date_output_dir = os.path.join(output_dir, sanitized_date)  # Create subdirectory for the date
    os.makedirs(date_output_dir, exist_ok=True)  # Ensure the directory exists

    date_data = df[df['date'] == date]

    for variable, label in [('leaf no.', 'Leaf Number'), ('petiole length mean (cm)', 'Petiole Length')]:
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

        # Save ANOVA results and assumptions
        with open(os.path.join(date_output_dir, f"{variable}_anova_results.txt"), "w") as f:
            f.write(f"ANOVA Results for {label} on {date}:\n")
            f.write(f"F-statistic: {anova_result.statistic}, p-value: {anova_result.pvalue}\n\n")
            f.write("Assumption Tests:\n")
            f.write(f"Shapiro-Wilk Test (Control): W={shapiro_control.statistic}, p={shapiro_control.pvalue}\n")
            f.write(f"Shapiro-Wilk Test (Shaded): W={shapiro_shaded.statistic}, p={shapiro_shaded.pvalue}\n")
            f.write(f"Levene's Test: W={levene_test.statistic}, p={levene_test.pvalue}\n")

        # Generate QQ plot
        plt.figure()
        stats.probplot(date_data[variable], dist="norm", plot=plt)
        plt.title(f"QQ Plot for {label} on {date}")
        plt.savefig(os.path.join(date_output_dir, f"{variable}_qq_plot.png"))
        plt.close()

        # Generate box plot
        plt.figure()
        sns.boxplot(x='treatment', y=variable, data=date_data)
        plt.title(f"Box Plot for {label} on {date}")
        plt.savefig(os.path.join(date_output_dir, f"{variable}_box_plot.png"))
        plt.close()

import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import os
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Load the data
file_path = "data/plant_measurements.csv"
df = pd.read_csv(file_path)
df['date'] = pd.to_datetime(df['date'], dayfirst=True)
df['date_str'] = df['date'].dt.strftime('%Y-%m-%d')
df = df.sort_values('date')

# Clean up any unnamed columns
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

output_dir = "statistics_output/"
os.makedirs(output_dir, exist_ok=True)

# Variables to analyze and plot
variables = [
    ('crown no.', 'Crown Number'),
    ('inflorescence no.', 'Inflorescence Number'),
    ('flower no.', 'Flower Number'),
    ('fruit no.', 'Fruit Number'),
    ('leaf no.', 'Leaf Number'),
    ('petiole length mean (cm)', 'Petiole Length (cm)'),
]

# ANOVA analysis and QQ plots
for variable, label in variables:
    variable_output_dir = os.path.join(output_dir, variable.replace(' ', '_'))
    os.makedirs(variable_output_dir, exist_ok=True)

    with open(os.path.join(variable_output_dir, f"{variable}_anova_results.txt"), "w") as summary_file:
        summary_file.write(f"ANOVA Results and Assumption Tests for {label}:\n")

        for date in df['date_str'].unique():
            date_data = df[df['date_str'] == date]

            if date_data[variable].dropna().empty:
                continue  # Skip if no data for this variable on this date

            try:
                # Fit OLS model
                model = ols(f'Q("{variable}") ~ C(treatment)', data=date_data).fit()
                anova_table = sm.stats.anova_lm(model, typ=2)

                # Extract values
                ss = anova_table["sum_sq"]
                df_ = anova_table["df"]
                ms = ss / df_
                f_val = anova_table["F"][0]
                p_val = anova_table["PR(>F)"][0]

                means = date_data.groupby("treatment")[variable].mean()

                summary_file.write(f"Date: {date}\n")
                summary_file.write(f"Means:\n")
                for treatment, mean_val in means.items():
                    summary_file.write(f"  {treatment.capitalize()}: {mean_val:.3f}\n")
                summary_file.write("\n")

                summary_file.write("ANOVA Table:\n")
                summary_file.write(f"{'Source':<15}{'DF':<6}{'SS':<12}{'MS':<12}{'F':<10}{'P-value':<10}\n")
                summary_file.write(f"{'Treatment':<15}{int(df_[0]):<6}{ss[0]:<12.3f}{ms[0]:<12.3f}{f_val:<10.3f}{'<0.001' if p_val < 0.001 else round(p_val, 3):<10}\n")
                summary_file.write(f"{'Residual':<15}{int(df_[1]):<6}{ss[1]:<12.3f}{ms[1]:<12.3f}{'':<10}{'':<10}\n")
                summary_file.write("\n")

                # Assumption checks
                control = date_data[date_data['treatment'] == 'control'][variable].dropna()
                shaded = date_data[date_data['treatment'] == 'shaded'][variable].dropna()

                if len(control) > 2 and len(shaded) > 2:
                    shapiro_control = stats.shapiro(control)
                    shapiro_shaded = stats.shapiro(shaded)
                    levene_test = stats.levene(control, shaded)

                    summary_file.write(f"Shapiro-Wilk (Control): W={shapiro_control.statistic:.3f}, p={'<0.001' if shapiro_control.pvalue < 0.001 else round(shapiro_control.pvalue, 3)}\n")
                    summary_file.write(f"Shapiro-Wilk (Shaded): W={shapiro_shaded.statistic:.3f}, p={'<0.001' if shapiro_shaded.pvalue < 0.001 else round(shapiro_shaded.pvalue, 3)}\n")
                    summary_file.write(f"Levene's Test: W={levene_test.statistic:.3f}, p={'<0.001' if levene_test.pvalue < 0.001 else round(levene_test.pvalue, 3)}\n")

                summary_file.write("\n")

                # QQ plot
                plt.figure()
                stats.probplot(date_data[variable].dropna(), dist="norm", plot=plt)
                plt.title(f"QQ Plot for {label} on {date}")
                plt.tight_layout()
                plt.savefig(os.path.join(variable_output_dir, f"{date}_qq_plot.png"))
                plt.close()

            except Exception as e:
                summary_file.write(f"Date: {date} - Error: {str(e)}\n\n")

# Plotting with skipped missing dates
plot_output_dir = os.path.join(output_dir, "line_plots")
os.makedirs(plot_output_dir, exist_ok=True)

marker_styles = {'control': 'o', 'shaded': 's'}
line_color = 'black'

for variable, label in variables:
    plt.figure(figsize=(6, 4))

    for treatment in df['treatment'].unique():
        sub_df = df[df['treatment'] == treatment]
        filtered = sub_df[["date_str", variable]].dropna()
        grouped = filtered.groupby('date_str').agg(mean=(variable, 'mean'), std=(variable, 'std')).reset_index()

        if not grouped.empty:
            face_color = 'black' if treatment == 'control' else 'white'
            edge_color = 'black'

            plt.errorbar(
                grouped['date_str'], grouped['mean'], yerr=grouped['std'],
                fmt=marker_styles[treatment], linestyle='-',
                color='black',  # line color
                markerfacecolor=face_color,
                markeredgecolor=edge_color,
                label=treatment.capitalize(), capsize=4,
                elinewidth=1, linewidth=1.5, markersize=6
)


    plt.xlabel('Date')
    plt.ylabel(label)
    plt.title(label)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(plot_output_dir, f"{variable.replace(' ', '_')}_lineplot.png"))
    plt.close()

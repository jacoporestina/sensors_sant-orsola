import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

# === PARAMETERS ===
input_file = 'input_statistics/termoigrometro.csv'
output_file = 'anova_termoigrometro.txt'
date_column = 'date'
treatment_column = 'treatment'
rep_column = 'rep'  # optional, but not used in analysis

# === LOAD DATA ===
df = pd.read_csv(input_file)

# Remove rows with missing data
df = df.dropna()

# Get variable columns (excluding date, treatment, rep)
variable_columns = [col for col in df.columns if col not in [date_column, treatment_column, rep_column]]

# === CREATE OUTPUT FILE ===
with open(output_file, 'w') as f:
    f.write(f"ANOVA and Assumption Tests by Date\n")
    f.write(f"{'='*60}\n")

    # Loop through each date
    for current_date, date_df in df.groupby(date_column):
        f.write(f"\nDate: {current_date}\n")
        f.write(f"{'='*60}\n")

        for var in variable_columns:
            f.write(f"\nVariable: {var}\n")
            f.write(f"{'-'*40}\n")

            try:
                # Fit linear model for treatment within the current date
                model = ols(f"{var} ~ C({treatment_column})", data=date_df).fit()
                anova_table = sm.stats.anova_lm(model, typ=2)

                # Extract ANOVA values
                df_treat = int(anova_table.iloc[0]['df'])
                df_resid = int(anova_table.iloc[1]['df'])
                ss_treat = anova_table.iloc[0]['sum_sq']
                ss_resid = anova_table.iloc[1]['sum_sq']
                ms_treat = ss_treat / df_treat
                ms_resid = ss_resid / df_resid
                f_value = anova_table.iloc[0]['F']
                p_value = anova_table.iloc[0]['PR(>F)']

                # Write ANOVA Table
                f.write("ANOVA Table:\n")
                f.write(f"{'Source':<12}{'DF':>6}{'SS':>12}{'MS':>12}{'F':>12}{'p-value':>12}\n")
                f.write(f"{'Treatment':<12}{df_treat:>6}{ss_treat:>12.4f}{ms_treat:>12.4f}{f_value:>12.4f}{p_value:>12.4f}\n")
                f.write(f"{'Residuals':<12}{df_resid:>6}{ss_resid:>12.4f}{ms_resid:>12.4f}\n")

                # Shapiro-Wilk Test (normality of residuals)
                shapiro_stat, shapiro_p = stats.shapiro(model.resid)
                f.write(f"\nShapiro-Wilk Test (Residuals): W = {shapiro_stat:.4f}, p = {shapiro_p:.4f}\n")

                # Bartlett Test (equal variances)
                groups = [group[var].values for name, group in date_df.groupby(treatment_column)]
                bart_stat, bart_p = stats.bartlett(*groups)
                f.write(f"Bartlett Test: Chi-sq = {bart_stat:.4f}, p = {bart_p:.4f}\n")

                # Summary statistics
                summary = date_df.groupby(treatment_column)[var].agg(['mean', 'std'])
                f.write("\nSummary Statistics:\n")
                f.write(f"{'Treatment':<12}{'Mean':>10}{'Std Dev':>12}\n")
                for idx, row in summary.iterrows():
                    f.write(f"{idx:<12}{row['mean']:>10.4f}{row['std']:>12.4f}\n")

            except Exception as e:
                f.write(f"Error analyzing {var} on {current_date}: {e}\n")

            f.write(f"{'-'*60}\n")

print(f"All results saved to: {output_file}")

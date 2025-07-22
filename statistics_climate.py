import pandas as pd
import scipy.stats as stats

# === PARAMETERS ===
input_file = 'input_statistics/termoigrometro.csv'
output_file = 'ttest_termoigrometro.txt'  # you may rename it to ttest_termoigrometro.txt
date_column = 'date'
treatment_column = 'treatment'
rep_column = 'rep'  # optional, not used

# === LOAD DATA ===
df = pd.read_csv(input_file)
df = df.dropna()

# Get variable columns (excluding date, treatment, rep)
variable_columns = [col for col in df.columns if col not in [date_column, treatment_column, rep_column]]

# === CREATE OUTPUT FILE ===
with open(output_file, 'w') as f:
    f.write(f"Independent t-test and Assumption Checks by Date\n")
    f.write(f"{'='*60}\n")

    for current_date, date_df in df.groupby(date_column):
        f.write(f"\nDate: {current_date}\n")
        f.write(f"{'='*60}\n")

        for var in variable_columns:
            f.write(f"\nVariable: {var}\n")
            f.write(f"{'-'*40}\n")

            try:
                # Split into two treatment groups
                groups = list(date_df[treatment_column].unique())
                if len(groups) != 2:
                    raise ValueError("Exactly two treatment groups are required for t-test.")

                group1 = date_df[date_df[treatment_column] == groups[0]][var]
                group2 = date_df[date_df[treatment_column] == groups[1]][var]

                # Perform independent t-test
                t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=True)

                f.write(f"Independent t-test:\n")
                f.write(f"{'Group 1':<12}: {groups[0]}\n")
                f.write(f"{'Group 2':<12}: {groups[1]}\n")
                f.write(f"{'t-statistic':<12}: {t_stat:.4f}\n")
                f.write(f"{'p-value':<12}: {p_value:.4f}\n")

                # Shapiro-Wilk test for normality (per group)
                shapiro1 = stats.shapiro(group1)
                shapiro2 = stats.shapiro(group2)
                f.write(f"\nShapiro-Wilk Test (Normality):\n")
                f.write(f"{groups[0]}: W = {shapiro1.statistic:.4f}, p = {shapiro1.pvalue:.4f}\n")
                f.write(f"{groups[1]}: W = {shapiro2.statistic:.4f}, p = {shapiro2.pvalue:.4f}\n")

                # Bartlett test for equal variances
                bart_stat, bart_p = stats.bartlett(group1, group2)
                f.write(f"\nBartlett Test (Equal Variance): Chi-sq = {bart_stat:.4f}, p = {bart_p:.4f}\n")

                # Summary statistics
                f.write(f"\nSummary Statistics:\n")
                f.write(f"{'Treatment':<12}{'Mean':>10}{'Std Dev':>12}\n")
                f.write(f"{groups[0]:<12}{group1.mean():>10.4f}{group1.std():>12.4f}\n")
                f.write(f"{groups[1]:<12}{group2.mean():>10.4f}{group2.std():>12.4f}\n")

            except Exception as e:
                f.write(f"Error analyzing {var} on {current_date}: {e}\n")

            f.write(f"{'-'*60}\n")

print(f"All results saved to: {output_file}")

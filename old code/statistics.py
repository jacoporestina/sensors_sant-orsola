import os
import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.graphics.gofplots import qqplot
import matplotlib.pyplot as plt

def create_folders():
    """Create folders for saving outputs."""
    os.makedirs("statistical_output", exist_ok=True)
    os.makedirs("qq_plots", exist_ok=True)

def run_anova_and_tests(dictionary_data):
    """
    Runs ANOVA, Shapiro-Wilk test, Levene's test, and generates QQ plots for each variable.
    Saves results in the 'statistical_output' folder and QQ plots in the 'qq_plots' folder.
    """
    create_folders()

    for variable, treatment_dict in dictionary_data.items():
        print(f"Processing variable: {variable}")

        # Prepare data for ANOVA
        monthly_data = []
        treatment_labels = []

        for treatment, repetition_dict in treatment_dict.items():
            for repetition, stats_dict in repetition_dict.items():
                for month, month_data in stats_dict['month'].items():
                    # Extract daily means for the month
                    daily_means = month_data['daily']['mean'].mean(axis=1).values
                    monthly_data.append(daily_means)
                    treatment_labels.extend([treatment] * len(daily_means))

        # Flatten the data for ANOVA
        monthly_data_flat = np.concatenate(monthly_data)

        # Create a DataFrame for ANOVA
        data = pd.DataFrame({
            'value': monthly_data_flat,
            'treatment': treatment_labels
        })

        # Perform ANOVA using statsmodels
        model = ols('value ~ C(treatment)', data=data).fit()
        anova_table = anova_lm(model)

        # Format the ANOVA table
        anova_table['p_value'] = anova_table['PR(>F)'].apply(lambda x: f"{x:.3f}")  # Ensure 3 decimal places
        print(f"ANOVA table for {variable}:\n{anova_table}")

        # Save ANOVA table to a file
        with open(f"statistical_output/{variable}_anova.txt", "w") as f:
            f.write(f"ANOVA table for {variable}:\n")
            f.write(anova_table.to_string())
            f.write("\n")

        # Calculate residuals (difference between observed and group means)
        residuals = model.resid

        # Perform Shapiro-Wilk test for normality of residuals
        shapiro_result = stats.shapiro(residuals)
        print(f"Shapiro-Wilk test result for {variable}: {shapiro_result}")

        # Save Shapiro-Wilk result
        with open(f"statistical_output/{variable}_shapiro.txt", "w") as f:
            f.write(f"Shapiro-Wilk test result for {variable}:\n")
            f.write(f"Test statistic: {shapiro_result.statistic}\n")
            f.write(f"p-value: {shapiro_result.pvalue:.3f}\n")  # Ensure 3 decimal places

        # Perform Levene's test for homogeneity of variances
        levene_result = stats.levene(*monthly_data)
        print(f"Levene's test result for {variable}: {levene_result}")

        # Save Levene's result
        with open(f"statistical_output/{variable}_levene.txt", "w") as f:
            f.write(f"Levene's test result for {variable}:\n")
            f.write(f"Test statistic: {levene_result.statistic}\n")
            f.write(f"p-value: {levene_result.pvalue:.3f}\n")  # Ensure 3 decimal places

        # Generate QQ plot for residuals
        plt.figure()
        qqplot(residuals, line='s')
        plt.title(f"QQ Plot for {variable} Residuals")
        plt.savefig(f"qq_plots/{variable}_qq_plot.png")
        plt.close()

        print(f"Completed processing for {variable}\n")
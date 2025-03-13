import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

def plot_overlay(df_control, df_shaded, column, month):
    """Plots control vs. shaded on the same plot, overlaying hourly averages of each day in the selected month."""
    comparison_folder = "plots/comparisons"
    os.makedirs(comparison_folder, exist_ok=True)

    # Filter data for the selected month
    df_control_month = df_control[df_control['Month'] == month]
    df_shaded_month = df_shaded[df_shaded['Month'] == month]

    plt.figure(figsize=(10, 6))

    # Loop through each day and plot separately for better visualization
    for date in df_control_month['Date'].unique():
        df_control_day = df_control_month[df_control_month['Date'] == date]
        df_shaded_day = df_shaded_month[df_shaded_month['Date'] == date]

        plt.plot(df_control_day['Hour'], df_control_day[column], label=f"Control {date}", color="orange", alpha=0.3)
        plt.plot(df_shaded_day['Hour'], df_shaded_day[column], label=f"Shaded {date}", color="blue", alpha=0.3)

    plt.xlabel("Time (Hourly)")
    plt.ylabel(column)
    plt.title(f"Overlay of {column} - {month} (Hourly Averages per Day)")
    plt.legend([], [], frameon=False)  # Hides individual legends to avoid clutter
    plt.grid(True)

    plt.savefig(f"plots/comparisons/{column}_Overlay_{month}.png", dpi=300)
    plt.close()


def plot_difference(df_control, df_shaded, column, month):
    """Computes and plots the hourly differences (Shaded - Control) per day in the selected month."""
    comparison_folder = "plots/comparisons"
    os.makedirs(comparison_folder, exist_ok=True)

    # Filter data for the selected month
    df_control_month = df_control[df_control['Month'] == month]
    df_shaded_month = df_shaded[df_shaded['Month'] == month]

    plt.figure(figsize=(10, 6))

    # Loop through each day and plot separately
    for date in df_control_month['Date'].unique():
        df_control_day = df_control_month[df_control_month['Date'] == date].set_index("Hour")
        df_shaded_day = df_shaded_month[df_shaded_month['Date'] == date].set_index("Hour")

        # Compute difference
        df_diff = df_shaded_day[column] - df_control_day[column]

        # Plot positive and negative differences in different colors
        plt.plot(df_diff[df_diff >= 0].index, df_diff[df_diff >= 0], color="green", label=f"Δ {column} {date} (Positive)", alpha=0.3)
        plt.plot(df_diff[df_diff < 0].index, df_diff[df_diff < 0], color="red", label=f"Δ {column} {date} (Negative)", alpha=0.3)

    plt.axhline(0, linestyle="--", color="black")

    plt.xlabel("Time (Hourly)")
    plt.ylabel(f"Δ {column}")
    plt.title(f"Difference (Shaded - Control) for {column} - {month} (Hourly Differences per Day)")
    plt.legend([], [], frameon=False)  # Hide individual legends for clarity
    plt.grid(True)

    plt.savefig(f"plots/comparisons/{column}_Difference_{month}.png", dpi=300)
    plt.close()



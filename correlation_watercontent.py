import pandas as pd
from file_processing import process_files

cvs_files = [
    "data/PoreWater_control.csv",
    "data/PoreWater_shaded.csv",
]

process_files(cvs_files)


def gravimetricWC(file_path):

    WATER_DENSITY = 1000  # g/L
    SUBSTRATE_BULK_DENSITY = 1591  # g/L
    SUBSTRATE_VOLUME = 15 # L

    df = pd.read_csv(file_path)

    if 'waterContent_mean' not in df.columns:
        raise ValueError("'waterContent_mean' column not found in the file.")

    # Remove rows with waterContent_mean == 0
    df = df[df["waterContent_mean"] != 0]

    # Calculate gravimetric water content
    df["gravimetricWC"] = df["waterContent_mean"] * (WATER_DENSITY / SUBSTRATE_BULK_DENSITY)

    # Calculate water weight per bag of plants
    df["water_weight"] = (df["waterContent_mean"] / 100) * SUBSTRATE_VOLUME * (WATER_DENSITY / 1000)

    output_path = file_path.replace(".csv", "_processed.csv")
    df.to_csv(output_path, index=False)

    print(f"Processed daily file saved to: {output_path}")
    return output_path

gravimetricWC("hourly_daily_data/PoreWater_control_hourly.csv")
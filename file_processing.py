import pandas as pd

def load_data(csv_files):
    """Loads CSV data, converts 'receivedAt' to datetime, and calculates both hourly and daily averages."""

    means_data = {}

    for variable, treatment in csv_files.items():
        # Create a subdictionary for each variable
        means_data[variable] = {}

        for treatment, file in treatment.items():
            # Load csv file into a Dataframe
            df = pd.read_csv(file, delimiter=';')
            print(df.head())

            #Transform receivedAt into readble pd dates
            df['receivedAt'] = pd.to_datetime(df['receivedAt'])
            print(df['receivedAt'].dtype)
            print(df.head())

            df.set_index('receivedAt', inplace=True)

            #Calculate hourly and daily means
            hourly_means = df.select_dtypes(include='number').resample('H').mean() #calculate hourly means, set data types to number to esclude columns with strings
            print(hourly_means)
            daily_means = df.select_dtypes(include='number').resample('D').mean()
            print(daily_means)

            # Store the hourly and daily means into the dictionary
            means_data[variable][treatment] = {
                'hourly': hourly_means,
                'daily' : daily_means
            }

    return means_data

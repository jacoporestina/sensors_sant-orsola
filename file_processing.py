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
            #print(df.head())

            # Transform receivedAt into readble pd dates
            df['receivedAt'] = pd.to_datetime(df['receivedAt'])
            #print(df['receivedAt'].dtype)
            #print(df.head())

            df.set_index('receivedAt', inplace=True)

            # If the variable is PAR, filter the data to include only the photoperiod (PAR > 0)
            if variable == 'photosyntheticallyActiveRadiation':
                df = df[df['photosyntheticallyActiveRadiation'] > 0]

            # Group data by month
            monthly_groups = df.groupby(pd.Grouper(freq='M'))

            # Initialize a dictionary to store monthly data
            monthly_data = {}

            # Loop through each month
            for month, month_data in monthly_groups:
                # Calculate hourly and daily means, max and min for the month
                daily_means_month = month_data.select_dtypes(include='number').resample('D').mean()
                daily_max_month = month_data.select_dtypes(include='number').resample('D').max()
                daily_min_month = month_data.select_dtypes(include='number').resample('D').min()

                # Store the monthly data
                monthly_data[month.strftime('%Y-%m')] = {
                    'daily' : {
                        'mean' : daily_means_month,
                        'max' : daily_max_month,
                        'min' : daily_min_month,
                    }
                }

            # Group the data by week
            weekly_groups = df.groupby(pd.Grouper(freq='W'))

            # Initialize a dictionary to store weekly data
            weekly_data = {}

            # Loop through each week
            for week, week_data in weekly_groups:
                # Calculate hourly and daily means for the week
                hourly_means_week = week_data.select_dtypes(include='number').resample('H').mean()
                hourly_max_week = week_data.select_dtypes(include='number').resample('H').max()
                hourly_min_week = week_data.select_dtypes(include='number').resample('H').min()

                # Store the weekly data
                weekly_data[week.strftime('%Y-%U')] = {
                    'hourly': {
                        'mean' : hourly_means_week,
                        'max' : hourly_max_week,
                        'min' : hourly_min_week
                    },
                }

            # Group the data by day
            daily_groups = df.groupby(pd.Grouper(freq='D'))

            # Initialize a dictionary to store daily data
            daily_data = {}

            # Loop through each day
            for day, day_data in daily_groups:
                # Calculate hourly means for the day
                hourly_means_day = day_data.select_dtypes(include='number').resample('H').mean()
                hourly_max_day = day_data.select_dtypes(include='number').resample('H').max()
                hourly_min_day = day_data.select_dtypes(include='number').resample('H').min()

                # Store the daily data
                daily_data[day.strftime('%Y-%m-%d')] = {
                    'hourly': {
                        'mean' : hourly_means_day,
                        'max' : hourly_max_day,
                        'min' : hourly_min_day,
                    }
                }

            # Store the monthly, weekly, and daily data into the dictionary
            means_data[variable][treatment] = {
                'month': monthly_data,
                'week': weekly_data,
                'day': daily_data,
            }

    return means_data

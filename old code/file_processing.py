import pandas as pd

def calculate_statistics(df, freq):
    """Helper function to calculate mean, max, and min for a given frequency."""
    stats = {
        'mean': df.select_dtypes(include='number').resample(freq).mean(),
        'max': df.select_dtypes(include='number').resample(freq).max(),
        'min': df.select_dtypes(include='number').resample(freq).min(),
    }
    return stats

def load_data(csv_files):
    """Loads CSV data, converts 'receivedAt' to datetime, and calculates hourly, daily, weekly, and monthly statistics."""
    dictionary_data = {}

    for variable, treatment_dict in csv_files.items():
        dictionary_data[variable] = {}

        for treatment, repetition_dict in treatment_dict.items():
            dictionary_data[variable][treatment] = {}

            for repetition, file in repetition_dict.items():
                # Load CSV file into a DataFrame
                df = pd.read_csv(file, delimiter=';')

                # Convert 'receivedAt' to datetime and set as index
                df['receivedAt'] = pd.to_datetime(df['receivedAt'])
                df.set_index('receivedAt', inplace=True)

                # Filter PAR data to include only the photoperiod (PAR > 0)
                if variable == 'photosyntheticallyActiveRadiation':
                    df = df[df['photosyntheticallyActiveRadiation'] > 0]

                # Initialize dictionaries to store statistics
                monthly_stats = {}
                weekly_stats = {}
                daily_stats = {}

                # Calculate monthly statistics
                monthly_groups = df.groupby(pd.Grouper(freq='M'))
                for month, month_data in monthly_groups:
                    monthly_stats[month.strftime('%Y-%m')] = {
                        'daily': calculate_statistics(month_data, 'D')
                    }

                # Calculate weekly statistics
                weekly_groups = df.groupby(pd.Grouper(freq='W'))
                for week, week_data in weekly_groups:
                    weekly_stats[week.strftime('%Y-%U')] = {
                        'hourly': calculate_statistics(week_data, 'H')
                    }

                # Calculate daily statistics
                daily_groups = df.groupby(pd.Grouper(freq='D'))
                for day, day_data in daily_groups:
                    daily_stats[day.strftime('%Y-%m-%d')] = {
                        'hourly': calculate_statistics(day_data, 'H')
                    }

                # Store the statistics in the dictionary
                dictionary_data[variable][treatment][repetition] = {
                    'month': monthly_stats,
                    'week': weekly_stats,
                    'day': daily_stats,
                }

    return dictionary_data

def calculate_means(dictionary_data):
    """
    Calculates means across repetitions for each variable, treatment, and time period.
    Returns a new dictionary without the 'repetition' key.
    """
    means_data = {}

    for variable, treatment_dict in dictionary_data.items():
        means_data[variable] = {}

        for treatment, repetition_dict in treatment_dict.items():
            means_data[variable][treatment] = {}

            # Initialize dictionaries to store aggregated statistics
            monthly_means = {}
            weekly_means = {}
            daily_means = {}

            # Iterate through repetitions to aggregate data
            for repetition, stats_dict in repetition_dict.items():
                # Aggregate monthly statistics
                for month, month_data in stats_dict['month'].items():
                    if month not in monthly_means:
                        monthly_means[month] = {'daily': {'mean': None, 'max': None, 'min': None}}

                    # Aggregate daily means for the month
                    if monthly_means[month]['daily']['mean'] is None:
                        monthly_means[month]['daily']['mean'] = month_data['daily']['mean']
                        monthly_means[month]['daily']['max'] = month_data['daily']['max']
                        monthly_means[month]['daily']['min'] = month_data['daily']['min']
                    else:
                        monthly_means[month]['daily']['mean'] += month_data['daily']['mean']
                        monthly_means[month]['daily']['max'] += month_data['daily']['max']
                        monthly_means[month]['daily']['min'] += month_data['daily']['min']

                # Aggregate weekly statistics
                for week, week_data in stats_dict['week'].items():
                    if week not in weekly_means:
                        weekly_means[week] = {'hourly': {'mean': None, 'max': None, 'min': None}}

                    # Aggregate hourly means for the week
                    if weekly_means[week]['hourly']['mean'] is None:
                        weekly_means[week]['hourly']['mean'] = week_data['hourly']['mean']
                        weekly_means[week]['hourly']['max'] = week_data['hourly']['max']
                        weekly_means[week]['hourly']['min'] = week_data['hourly']['min']
                    else:
                        weekly_means[week]['hourly']['mean'] += week_data['hourly']['mean']
                        weekly_means[week]['hourly']['max'] += week_data['hourly']['max']
                        weekly_means[week]['hourly']['min'] += week_data['hourly']['min']

                # Aggregate daily statistics
                for day, day_data in stats_dict['day'].items():
                    if day not in daily_means:
                        daily_means[day] = {'hourly': {'mean': None, 'max': None, 'min': None}}

                    # Aggregate hourly means for the day
                    if daily_means[day]['hourly']['mean'] is None:
                        daily_means[day]['hourly']['mean'] = day_data['hourly']['mean']
                        daily_means[day]['hourly']['max'] = day_data['hourly']['max']
                        daily_means[day]['hourly']['min'] = day_data['hourly']['min']
                    else:
                        daily_means[day]['hourly']['mean'] += day_data['hourly']['mean']
                        daily_means[day]['hourly']['max'] += day_data['hourly']['max']
                        daily_means[day]['hourly']['min'] += day_data['hourly']['min']

            # Calculate the mean by dividing by the number of repetitions
            num_repetitions = len(repetition_dict)

            for month in monthly_means:
                monthly_means[month]['daily']['mean'] /= num_repetitions
                monthly_means[month]['daily']['max'] /= num_repetitions
                monthly_means[month]['daily']['min'] /= num_repetitions

            for week in weekly_means:
                weekly_means[week]['hourly']['mean'] /= num_repetitions
                weekly_means[week]['hourly']['max'] /= num_repetitions
                weekly_means[week]['hourly']['min'] /= num_repetitions

            for day in daily_means:
                daily_means[day]['hourly']['mean'] /= num_repetitions
                daily_means[day]['hourly']['max'] /= num_repetitions
                daily_means[day]['hourly']['min'] /= num_repetitions

            # Store the aggregated statistics in the means_data dictionary
            means_data[variable][treatment] = {
                'month': monthly_means,
                'week': weekly_means,
                'day': daily_means,
            }

    return means_data

def transform_csv(data):
    """Function to flatten the nested dictionary into a list of rows"""
    dictionary_data_to_csv = []
    for variable, treatment_dict in data.items():
        for treatment, repetition_dict in treatment_dict.items():
            for repetition, time_dict in repetition_dict.items():
                for time_period, time_data in time_dict.items():
                    for timestamp, stats_dict in time_data.items():
                        for stat_type, values in stats_dict.items():
                            row = {
                                "variable": variable,
                                "treatment": treatment,
                                "repetition": repetition,
                                "time_period": time_period,
                                "timestamp": timestamp,
                                "stat_type": stat_type,
                                "mean": values["mean"],
                                "max": values["max"],
                                "min": values["min"]
                            }
                            dictionary_data_to_csv.append(row)
    return dictionary_data_to_csv


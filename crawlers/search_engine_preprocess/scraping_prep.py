import pandas as pd
import random

def csv_to_array_of_strings(csv_file_path):
    school_array = []
    df = pd.read_csv(csv_file_path)
    try:
        print(df)
        for index, row in df.iterrows():
            concatenated_row = f"{str(row.iloc[0])} website "
            rest_of_row = ' '.join([str(item) for item in row.iloc[1:]])  
            concatenated_row += rest_of_row
            school_array.append(concatenated_row)
        return school_array
    
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

def csv_to_array_of_strings_sample(csv_file_path, sample_size):
    full_school_array = csv_to_array_of_strings(csv_file_path)
    print(full_school_array)
    
    if sample_size > len(full_school_array):
        raise ValueError()
    
    return random.sample(full_school_array, sample_size)
    
    
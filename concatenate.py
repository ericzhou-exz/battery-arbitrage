import os
import pandas as pd

# Automatically navigate to the current directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Directory containing the CSV files (in this case, the same directory as the script)
folder = '/sa'
csv_dir = script_dir + folder

# List all CSV files in the directory
csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]

# Check if there are 12 CSV files in the directory
if len(csv_files) != 12:
    print(f"Error: Expected 12 CSV files, but found {len(csv_files)}.")
else:
    # Initialize an empty list to hold dataframes
    dataframes = []

    # Iterate over the CSV files
    for i, file in enumerate(csv_files):
        file_path = os.path.join(csv_dir, file)
        if i == 0:
            # For the first file, read with header
            df = pd.read_csv(file_path)
        else:
            # For subsequent files, skip the header row
            df = pd.read_csv(file_path, header=0)
        dataframes.append(df)

    # Concatenate all dataframes
    concatenated_df = pd.concat(dataframes, ignore_index=True)

    # Save the concatenated dataframe to a new CSV file
    output_file = os.path.join(csv_dir, 'concatenated_output.csv')
    concatenated_df.to_csv(output_file, index=False)

    print(f'Concatenated CSV saved to {output_file}')

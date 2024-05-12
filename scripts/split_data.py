import os
import pandas as pd
import numpy as np


def split_dataset():
    output_folder = "../data_raw/Ingestion"
    num_files = 200
    dataset_path = "../data_raw/data_with_errors.csv"
    try:
        df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        print(f"Error: Dataset file '{dataset_path}' not found.")
        return

    # Shuffle the DataFrame rows
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    os.makedirs(output_folder, exist_ok=True)

    num_rows_per_file = len(df) // num_files

    for i in range(num_files):
        start_idx = i * num_rows_per_file
        end_idx = (i + 1) * num_rows_per_file if i < num_files - 1 else len(df)
        subset = df.iloc[start_idx:end_idx]
        subset.to_csv(os.path.join(output_folder, f"data_{i + 1}.csv"), index=False)

    print(f"Dataset split into {num_files} files in the '{output_folder}' folder.")

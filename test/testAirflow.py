import os
import random
import pandas as pd

ingestion_folder = "../data_raw/Ingestion"
files = os.listdir(ingestion_folder)

file_set = set()

for _ in range(100):
    selected_file = random.choice(files)
    file_path = os.path.join(ingestion_folder, selected_file)

    if file_path not in file_set:
        file_set.add(file_path)
        df = pd.read_csv(file_path)
    else:
        break

print(file_set)

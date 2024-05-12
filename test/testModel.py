import pandas as pd
from train import train

df = pd.read_csv(
    "/Users/ericwindsor/Documents/EPITA_ERIC/Data_Scicence_Production/DSP_Final/data_raw/train.csv"
)
res = train(df)
print(res)

import great_expectations as ge
import pandas as pd
from scripts.great_expectation import validate_data, send_teams_alert
from scripts.save_log import save_data_logs

# Load your dataset into a Pandas DataFrame
input_data_df = pd.read_csv("../data_raw/Ingestion/data_12.csv")
errors = validate_data(input_data_df)
send_teams_alert(errors)
save_data_logs(errors)
# Build data docs


# Print validation results

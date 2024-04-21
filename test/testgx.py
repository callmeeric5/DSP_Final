import great_expectations as ge
import pandas as pd

# Load your dataset into a Pandas DataFrame
input_data_df = pd.read_csv("../data_raw/Ingestion/data_1.csv")

# Initialize the Great Expectations DataContext
context = ge.data_context.DataContext()

# Run validation on the dataset using the Black Friday expectation suite
validation_results = context.run_validation_operator(
    "action_list_operator",
    assets_to_validate=[input_data_df],
    run_id="black_friday_validation",
)

# Review the validation results
print(validation_results)

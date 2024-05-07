import great_expectations as gx
import pandas as pd
from datetime import datetime
import requests
from great_expectations.core.batch import RuntimeBatchRequest


def validate_data(df):
    context = gx.get_context()
    batch_request = RuntimeBatchRequest(
        datasource_name="black_friday",
        data_connector_name="default_runtime_data_connector_name",
        data_asset_name="black_friday",
        runtime_parameters={"batch_data": df},
        batch_identifiers={"runtime_batch_identifier_name": "default_identifier"},
    )

    validation_results = context.run_checkpoint(
        checkpoint_name="black_friday_checkpoint",
        validations=[
            {
                "batch_request": batch_request,
                "expectation_suite_name": "black_friday.csv.warning",
            }
        ],
    )
    errors = {}
    invalid_rows_data = pd.DataFrame(columns=df.columns)
    for result_id, result_data in validation_results["run_results"].items():
        validation_result = result_data["validation_result"]

        for expectation_result in validation_result["results"]:
            if not expectation_result["success"]:
                column = expectation_result["expectation_config"]["kwargs"].get(
                    "column"
                )
                if column is not None and column in df.columns:
                    result_info = expectation_result["result"]
                    partial_unexpected_list = result_info.get(
                        "partial_unexpected_list", []
                    )
                    if partial_unexpected_list:
                        invalid_rows_data = pd.concat(
                            [
                                invalid_rows_data,
                                df[df[column].isin(partial_unexpected_list)],
                            ]
                        )
                    errors[column] = {
                        "missing_percent": result_info.get("missing_percent", 0.0),
                        "unexpected_percent": result_info.get(
                            "unexpected_percent", 0.0
                        ),
                    }

    return errors


input_data_df = pd.read_csv("../data_raw/Ingestion/data_3.csv")
res = validate_data(input_data_df)
print(res)

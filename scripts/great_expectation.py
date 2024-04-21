import great_expectations as gx
import pandas as pd
from datetime import datetime
import requests

from great_expectations.core.batch import RuntimeBatchRequest


def validate_data(df):
    batch_request = RuntimeBatchRequest(
        datasource_name="black_friday",
        data_connector_name="default_runtime_data_connector_name",
        data_asset_name="black_friday",
        runtime_parameters={"batch_data": df},
        batch_identifiers={"runtime_batch_identifier_name": "default_identifier"},
    )
    context = gx.get_context()
    validator = context.get_validator(
        batch_request=batch_request, expectation_suite_name="black_friday.csv.warning"
    )

    validation_results = validator.validate()
    errors = []
    invalid_rows_data = pd.DataFrame(columns=df.columns)
    for expectation_result in validation_results["results"]:
        if not expectation_result["success"]:
            column = find_column_key(expectation_result["expectation_config"]["kwargs"])
            if "partial_unexpected_list" in expectation_result["result"]:
                ls = expectation_result["result"]["partial_unexpected_list"]
                invalid_rows_data = pd.concat(
                    [invalid_rows_data, df[df[column].isin(ls)]]
                )
                missing_percent = expectation_result["result"].get(
                    "missing_percent", "N/A"
                )
                unexpected_percent = expectation_result["result"].get(
                    "unexpected_percent", "N/A"
                )

                errors.append(
                    f"Validation failed for column '{column}', missing percent: {missing_percent}, "
                    f"unexpected_percent: {unexpected_percent}"
                )

            else:
                errors.append(
                    "No partial unexpected list found for column: {}".format(column)
                )
    filepath_bad = (
        f"/Users/ericwindsor/Documents/EPITA_ERIC/Data_Scicence_Production"
        f"/DSP_Final/data_raw/split_data/Bad_Data/{datetime.now()}.csv"
    )
    filepath_clean = (
        f"/Users/ericwindsor/Documents/EPITA_ERIC/Data_Scicence_Production"
        f"/DSP_Final/data_raw/split_data/Clean_Data/{datetime.now()}.csv"
    )
    df.drop(invalid_rows_data.index, inplace=True)
    df.to_csv(filepath_clean, index=False)
    invalid_rows_data.to_csv(filepath_bad, index=False)
    # print(validation_results)
    return errors


def find_column_key(kwargs_dict):
    for key, value in kwargs_dict.items():
        if isinstance(value, str) and "column" in key.lower():
            return value
    return None


def send_teams_alert(errors):
    webhook_url = (
        "https://epitafr.webhook.office.com/webhookb2/"
        "c291b763-1eb0-48f6-85ae-652bc5ad8949@3534b3d7-316c-4bc9-9ede-605c860f49d2/"
        "IncomingWebhook/0b2445947a6342489b4d086b6e67e64e/275af251-9494-48df-a4d0-6ba6842636fc"
    )
    errors = [str(error) for error in errors]
    error_message = "\n".join(errors)

    payload = {
        "text": f"Data validation failed with the following errors:\n{error_message}"
    }

    try:
        response = requests.post(webhook_url, json=payload)

        if response.status_code == 200:
            print("Alert sent successfully to Teams channel.")
        else:
            print(
                f"Failed to send alert to Teams channel. Status code: {response.status_code}"
            )
            print(f"Response content: {response.content}")
    except Exception as e:
        print(f"An error occurred while sending the alert: {e}")


# # # # Load the input data
# input_data_df = pd.read_csv("../data_raw/Ingestion/data_55.csv")
# #
# # Validate the data
# errors = validate_data(input_data_df)
#
# # Send alert if validation failed
# if errors:
#     send_teams_alert(errors)

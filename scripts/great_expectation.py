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

    print(validation_results)
    context.build_data_docs()
    invalid_rows_data = pd.DataFrame(columns=df.columns)
    run_id = validation_results["run_id"]
    run_stats = None
    documentation_link = None
    errors = {}
    for result_id, result_data in validation_results["run_results"].items():

        if "black_friday" in result_data["validation_result"]["meta"]["active_batch_definition"]["data_asset_name"]:
            validation_result = result_data["validation_result"]
            if run_stats is None:
                run_stats = validation_result.get("statistics", {})
            if documentation_link is None:
                documentation_link = result_data["actions_results"]["update_data_docs"][
                    "local_site"
                ]
            for expectation_result in validation_result["results"]:
                if not expectation_result["success"]:
                    column = expectation_result["expectation_config"]["kwargs"].get(
                        "column"
                    )
                    error_type = expectation_result.expectation_config.expectation_type
                    result_info = expectation_result["result"]
                    partial_unexpected_list = result_info.get("partial_unexpected_list", [])
                    invalid_rows_data = pd.concat(
                        [invalid_rows_data, df[df[column].isin(partial_unexpected_list)]]
                    )
                    if column not in errors:
                        errors[column] = {
                            "error_types": [],
                            "missing_percent": result_info.get("missing_percent", 0.0),
                            "unexpected_percent": result_info.get("unexpected_percent", 0.0),
                        }

                    if error_type not in errors[column]["error_types"]:
                        errors[column]["error_types"].append(error_type)

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
    meta_info = {
        "html": documentation_link,
        "run_id": getattr(run_id, "run_name", "N/A"),
        "run_time": getattr(run_id, "run_time", "N/A"),
        "statistics": run_stats,
    }

    final_report = {"meta": meta_info, "errors": errors}
    return final_report


def send_teams_alert(report):
    webhook_url = (
        "https://epitafr.webhook.office.com/webhookb2/"
        "c291b763-1eb0-48f6-85ae-652bc5ad8949@3534b3d7-316c-4bc9-9ede-605c860f49d2/"
        "IncomingWebhook/0b2445947a6342489b4d086b6e67e64e/275af251-9494-48df-a4d0-6ba6842636fc"
    )
    # print(report)
    meta_info = report.get("meta")
    errors = report.get("errors")
    message_lines = [
        f"**Documentation**: {meta_info['html']}",
        f"**Run ID**: {meta_info['run_id']}",
        f"**Run Time**: {meta_info['run_time']}",
        f"**Statistics**: {meta_info['statistics']}",
    ]

    for column, error_details in errors.items():
        message_lines.append(
            f"Column: {column},Error_types:{error_details['error_types']} Missing Percent: {error_details['missing_percent']}, Unexpected Percent: "
            f"{error_details['unexpected_percent']}"
        )

    message = "<br>".join(message_lines)
    payload = {"text": message}

    response = requests.post(webhook_url, json=payload)
    if response.status_code == 200:
        print("Alert sent successfully to Teams channel.")
    else:
        print(
            f"Failed to send alert to Teams channel. Status code: {response.status_code}, Response: {response.text}"
        )

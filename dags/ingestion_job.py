import pandas as pd
import os 
import logging
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.models import Variable

#from airflow.utils.session import push as XCom_push

from datetime import timedelta

full_path = "/opt/airflow/data_ingestion_folder"  #../data_ingestion_folder
#full_path = os.path.join(os.getcwd(), path)

@dag(
    dag_id='dsp_example',
    description='DSP Example DAG',
    tags=['dsp'],
    schedule_interval=timedelta(minutes=5),
    start_date=days_ago(0, hour=1)
)

def ingestion_job():
    expected_columns = ['User_ID', 'Product_ID', 'Gender', 'Age', 'Occupation', 'City_Category',
                        'Stay_In_Current_City_Years', 'Marital_Status', 'Product_Category_1',
                        'Product_Category_2', 'Product_Category_3']
    obligatory_data = ["User_ID", "Product_ID", "Gender", "Age", "Occupation", "City_Category", "Stay_In_Current_City_Years", "Marital_Status","Product_Category_1"]
    out_put = ["Purchase"]
    optional_data = ["Product_Category_2", "Product_Category_3"]
    #@task
    # def folder_check():
    #     train_paths = {}
    #     test_paths = {}
    #     for file_name in os.listdir(full_path):
    #         if ("test" in file_name or "inference" in file_name) and file_name not in test_paths:
    #             test_paths[file_name] = False
    #         elif "train" in file_name and file_name not in train_paths:
    #             train_paths[file_name] = False
    #     return {'dataframe': None, 'processed_paths': {'train_paths': train_paths, 'test_paths': test_paths}}
    
    # @task
    # def read_csv_files(paths_dict):
    #     df = pd.DataFrame()
    #     for path, processed in paths_dict.items():
    #         if not processed:
    #             new_df = pd.read_csv(path)
    #             if set(new_df.columns) == set(expected_columns):
    #                 df = pd.concat([df, new_df], ignore_index=True)
    #                 paths_dict[path] = True
    #     return {'dataframe': df, 'processed_paths': paths_dict}
    @task
    def folder_check():
        train_paths = {}
        test_paths = {}
        for file_name in os.listdir(full_path):
            file_name=file_name.lower().strip()
            if "test" in file_name or "inference" in file_name:
                test_paths[os.path.join(full_path, file_name)] = False
            elif "train" in file_name:
                train_paths[os.path.join(full_path, file_name)] = False
        return {'train_paths': train_paths, 'test_paths': test_paths}
    @task
    def log_folder_check_result(folder_check_output):
        if folder_check_output['train_paths']:
            logging.info("Train paths are present.")
        else:
            logging.info("No train paths found.")
    # @task
    # def read_csv_files(paths_dict):
    #     logging.info(f"Received paths_dict: {paths_dict}")
    #     df = pd.DataFrame()
    #     for path, processed in paths_dict.items():
    #         if not processed:
    #             new_df = pd.read_csv(path)
    #             if set(new_df.columns) == set(expected_columns):
    #                 df = pd.concat([df, new_df], ignore_index=True)
    #                 paths_dict[path] = True
    #     return {'dataframe': df, 'processed_paths': paths_dict}
    @task
    def read_csv_files(folder_check_output):
        train_paths = folder_check_output['train_paths']
        test_paths = folder_check_output['test_paths']
        train_df = pd.DataFrame()
        test_df = pd.DataFrame()

        for path in train_paths:
            new_df = pd.read_csv(path)
            if set(new_df.columns) == set(expected_columns+out_put):
                train_df = pd.concat([train_df, new_df], ignore_index=True)

        for path in test_paths:
            new_df = pd.read_csv(path)
            if set(new_df.columns) == set(expected_columns):
                test_df = pd.concat([test_df, new_df], ignore_index=True)

        return {'train_df': train_df, 'test_df': test_df}
    # @task
    # def anomaly_check(input_data, is_inference):
    #     check_columns = obligatory_data + (out_put if not is_inference else [])
    #     null_rows_mask = input_data[check_columns].isnull().any(axis=1)
    #     df_with_nulls = input_data[null_rows_mask]
    #     condition = (
    #         input_data['Gender'].isin(['M', 'F']) &
    #         input_data['Product_Category_1'].between(1, 18) &
    #         (input_data['Product_Category_2'].isnull() | input_data['Product_Category_2'].between(2, 18)) &
    #         (input_data['Product_Category_3'].isnull() | input_data['Product_Category_3'].between(3, 18)) &
    #         input_data['City_Category'].isin(['A', 'B', 'C']) &
    #         input_data['Marital_Status'].isin([0, 1]) &
    #         input_data['Occupation'].between(0, 20)
    #     )
    #     if is_inference is False:
    #         condition &= input_data[out_put[0]] > 0
    #     df_with_value_issues = input_data[~condition]

    #     if is_inference is True:
    #         df_issues = pd.concat([df_with_nulls, df_with_value_issues]).drop_duplicates()
    #     elif is_inference is False:
    #         negative_values = input_data[out_put[0]] <= 0
    #         df_negative_values = input_data[negative_values]
    #         df_issues = pd.concat([df_with_nulls, df_with_value_issues, df_negative_values]).drop_duplicates()
    #     input_data_cleaned = input_data.drop(df_issues.index)
    #     return {'df_issues': df_issues, 'input_data_cleaned': input_data_cleaned}
    @task
    def anomaly_check(dataframes_dict, is_inference):
        input_data = dataframes_dict['train_df'] if not is_inference else dataframes_dict['test_df']
        # out_put = ["Purchase"]
        check_columns=obligatory_data.copy()
        if is_inference is False:
            check_columns.append("Purchase")
        null_rows_mask = input_data[obligatory_data].isnull().any(axis=1)
        df_with_nulls = input_data[null_rows_mask]
        condition = (
            input_data['Gender'].isin(['M', 'F']) &
            input_data['Product_Category_1'].between(1, 18) &
            (input_data['Product_Category_2'].isnull() | input_data['Product_Category_2'].between(2, 18)) &
            (input_data['Product_Category_3'].isnull() | input_data['Product_Category_3'].between(3, 18)) &
            input_data['City_Category'].isin(['A', 'B', 'C']) &
            input_data['Marital_Status'].isin([0, 1]) &
            input_data['Occupation'].between(0, 20)
        )
        if not is_inference:
            condition &= input_data[out_put[0]] > 0
        df_with_value_issues = input_data[~condition]
        # if is_inference is True:
        #     df_issues = pd.concat([df_with_nulls, df_with_value_issues]).drop_duplicates()
        # elif is_inference is False:
        #     negative_values = input_data[out_put[0]] <= 0
        #     df_negative_values = input_data[negative_values]
        #     df_issues = pd.concat([df_with_nulls, df_with_value_issues, df_negative_values]).drop_duplicates()
        # input_data_cleaned = input_data.drop(df_issues.index)
        df_issues = pd.concat([df_with_nulls, df_with_value_issues]).drop_duplicates() if not df_with_nulls.empty or not df_with_value_issues.empty else pd.DataFrame()
        input_data_cleaned = input_data.drop(df_issues.index) if not df_issues.empty else input_data
        return {'df_issues': df_issues, 'input_data_cleaned': input_data_cleaned}
    # @task
    # def append_df_to_csv(df_issues, input_data_cleaned, file_type):
    #     df_issues_path = os.path.join(full_path, f'anomaly_{file_type}.csv')
    #     input_data_cleaned_path = os.path.join(full_path, f'noissue_{file_type}.csv')
    
    #     if os.path.exists(df_issues_path):
    #         df_issues.to_csv(df_issues_path, mode='a', header=False, index=False)
    #     else:
    #         df_issues.to_csv(df_issues_path, mode='w', header=True, index=False)
    
    #     if os.path.exists(input_data_cleaned_path):
    #         input_data_cleaned.to_csv(input_data_cleaned_path, mode='a', header=False, index=False)
    #     else:
    #         input_data_cleaned.to_csv(input_data_cleaned_path, mode='w', header=True, index=False)
    
    #     return {
    #         "df_issues_path": df_issues_path,
    #         "input_data_cleaned_path": input_data_cleaned_path
    #     }
    @task
    def append_df_to_csv(result_dict, file_type):
        df_issues_path = os.path.join(full_path, f'anomaly_{file_type}.csv')
        input_data_cleaned_path = os.path.join(full_path, f'noissue_{file_type}.csv')

        # result_dict['df_issues'].to_csv(df_issues_path, mode='w', header=True, index=False)
        # result_dict['input_data_cleaned'].to_csv(input_data_cleaned_path, mode='w', header=True, index=False)

        # return {
        #     "df_issues_path": df_issues_path,
        #     "input_data_cleaned_path": input_data_cleaned_path
        # }
        if not result_dict['df_issues'].empty:
            result_dict['df_issues'].to_csv(df_issues_path, mode='w', header=True, index=False)
        if not result_dict['input_data_cleaned'].empty:
            result_dict['input_data_cleaned'].to_csv(input_data_cleaned_path, mode='w', header=True, index=False)

        return {
            "df_issues_path": df_issues_path,
            "input_data_cleaned_path": input_data_cleaned_path
        }
    
    # folder_check_output = folder_check()
    # csv_files_output = read_csv_files(folder_check_output)
    
    # train_anomaly_check_output = anomaly_check(csv_files_output, False)
    # test_anomaly_check_output = anomaly_check(csv_files_output, True)
    
    # append_df_to_csv(train_anomaly_check_output, 'train')
    # append_df_to_csv(test_anomaly_check_output, 'test')

    # folder_check_output = folder_check()
    # train_paths, test_paths = folder_check_output['processed_paths']['train_paths'], folder_check_output['processed_paths']['test_paths']

    # train_df, train_paths = read_csv_files(train_paths)['dataframe'], read_csv_files(train_paths)['processed_paths']
    # test_df, test_paths = read_csv_files(test_paths)['dataframe'], read_csv_files(test_paths)['processed_paths']

    # train_anomaly_check_output = anomaly_check(train_df, False)
    # test_anomaly_check_output = anomaly_check(test_df, True)
    # train_df_issues, train_df_cleaned = train_anomaly_check_output['df_issues'], train_anomaly_check_output['input_data_cleaned']
    # append_df_to_csv(train_df_issues, train_df_cleaned, 'train')
    # test_df_issues, test_df_cleaned = test_anomaly_check_output['df_issues'], test_anomaly_check_output['input_data_cleaned']
    # append_df_to_csv(test_df_issues, test_df_cleaned, 'test')

    """
    folder_check_output = folder_check()
    log_folder_check_result(folder_check_output)

    # train_path_output = folder_check_output['train_paths']
    # test_path_output = folder_check_output['test_paths']
    # train_df = read_csv_files(train_path_output)
    # test_df = read_csv_files(test_path_output)
    csv_files_output = read_csv_files(folder_check_output)
    train_df = csv_files_output['train_df']
    test_df = csv_files_output['test_df']

    train_anomaly_check_output = anomaly_check(train_df, False)
    test_anomaly_check_output = anomaly_check(test_df, True)
    
    append_df_to_csv(train_anomaly_check_output['df_issues'], train_anomaly_check_output['input_data_cleaned'], 'train')
    append_df_to_csv(test_anomaly_check_output['df_issues'], test_anomaly_check_output['input_data_cleaned'], 'test')
    """
    folder_check_output = folder_check()
    csv_files_output = read_csv_files(folder_check_output)
    
    train_anomaly_check_output = anomaly_check(csv_files_output, False)
    test_anomaly_check_output = anomaly_check(csv_files_output, True)
    
    append_df_to_csv(train_anomaly_check_output, 'train')
    append_df_to_csv(test_anomaly_check_output, 'test')


ingestion_job_dag = ingestion_job()

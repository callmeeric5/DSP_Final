import pandas as pd
import os 

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago


@dag(
    dag_id='dsp_example',
    description='DSP Example DAG',
    tags=['dsp'],
    #schedule=timedelta(minutes=5)
    #start_date=days_ago(n=0, hour=1)
)

def ingestion_job():
    expected_columns = ['User_ID', 'Product_ID', 'Gender', 'Age', 'Occupation', 'City_Category',
                        'Stay_In_Current_City_Years', 'Marital_Status', 'Product_Category_1',
                        'Product_Category_2', 'Product_Category_3', 'Purchase']
    obligatory_data = ["User_ID", "Product_ID", "Gender", "Age", "Occupation", "City_Category", "Stay_In_Current_City_Years", "Marital_Status","Product_Category_1"]
    out_put = ["Purchase"]
    optional_data = ["Product_Category_2", "Product_Category_3"]
    train_df=pd.DataFrame
    test_df=pd.DataFrame
    train_paths=dict()
    test_paths=dict()
    folder_path=r'C:\Users\SADEK COMPUTER\Desktop\Epita\01 - Semester 2\Data Science Production\DSP - Final Project\dags\data_ingestion_folder'
    index=1
    @task
    def folder_check():
        for file_name in os.listdir(folder_path):
            if ("test" in file_name | "inference" in file_name) & file_name not in test_paths:
                test_paths[file_name]=False
            elif ("train" in file_name) & file_name not in train_paths:
                train_paths[file_name]=False
    @task
    def appending_df(paths_dict:dict, datframe:pd.DataFrame):
        for path, processed in paths_dict.items():
            if processed is False:
                new_df=pd.read_csv(path)
                if set(new_df.columns)==expected_columns:
                    dataframe=pd.concat([dataframe,new_df],ignore_index=True)
                    paths_dict[path]=True
        return dataframe
    @task
    def anomaly_check(input_data:pd.DataFrame,is_inference:bool):
        check_columns = obligatory_data + (out_put if not is_inference else [])
        null_rows_df = input_data[check_columns].isnull().any(axis=1)
        df_with_nulls = input_data[null_rows_df]
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
            condition &= (input_data[out_put[0]] > 0)
        df_with_value_issues = input_data[~condition]
        if is_inference is False:
            negative_values=input_data[out_put[0]]<=0
            df_negative_values=input_data[negative_values]
            df_issues=pd.concat([df_with_nulls, df_with_value_issues,df_negative_values]).drop_duplicates()
        else:
            df_issues = pd.concat([df_with_nulls, df_with_value_issues]).drop_duplicates()
        input_data_cleaned = input_data.drop(df_issues.index)
        return df_issues, input_data_cleaned
    
    
    folder_check()
    train_df=appending_df(train_paths,train_df)
    test_df=appending_df(test_paths,test_df)
    #got the final form of the train and test 
    train_df_anomaly,train_df_final=anomaly_check(train_df,False)
    test_df_anomaly,test_df_final=anomaly_check(test_df,True)
    """
    1. put all the anomalies in the database
    2. We can append train_df_final and test_df_final 
    to the data folder
    """
    train_df_anomaly.to_csv(folder_path+'/anomaly_train_'+index)
    train_df_final.to_csv(folder_path+'/noissue_train_'+index)
    test_df_anomaly.to_csv(folder_path+'/anomaly_test_'+index)
    test_df_final.to_csv(folder_path+'/noissue_test_'+index)

ingestion_job_work = ingestion_job()

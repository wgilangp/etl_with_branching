from airflow.decorators import dag
from airflow.operators.python import PythonOperator, BranchPythonOperator
from sqlalchemy import create_engine
from datetime import datetime
import os
import pandas as pd
import kagglehub

# Function to extract data from Kaggle
def extract_data_from_kaggle(dataset, **kwargs):
    if dataset == "walmart":
        # Download the Walmart dataset
        path = kagglehub.dataset_download("umerhaddii/walmart-stock-data-2024")
        dataset_file = os.path.join(path, "wmt_data.csv")
        df = pd.read_csv(dataset_file)
    elif dataset == "instagram":
        # Download the Instagram dataset
        path = kagglehub.dataset_download("ankulsharma150/marketing-analytics-project")
        dataset_file = os.path.join(path, "Instagram-Data.csv")
        df = pd.read_csv(dataset_file)
    
    # Save the DataFrame to CSV in the staging area
    save_path = f"data/{dataset}.csv"
    df.to_csv(save_path, index=False)
    return save_path

# Function to load data into SQLite
def load_to_sqlite(dataset, **kwargs):
    engine = create_engine(f"sqlite:///data/{dataset}.db")
    file_path = f"data/{dataset}.csv"
    
    # Load data into SQLite (e.g., pandas read_csv and to_sql)
    df = pd.read_csv(file_path)
    df.to_sql(dataset, con=engine, if_exists='replace', index=False)
    
    return f"{dataset}.db"

# Function to choose which dataset to extract based on Run Config Param
def choose_branch(**kwargs):
    if kwargs['params']['dataset'] == 'walmart':
        return 'extract_walmart_data'
    else:
        return 'extract_instagram_data'

# DAG Definition
@dag(
    dag_id='etl_with_branching',
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    params={
        "dataset": "walmart",  # Default value
    }
)
def etl_with_branching():
    
    # Branching task to choose between datasets
    choose_branch_task = BranchPythonOperator(
        task_id='choose_dataset_branch',
        python_callable=choose_branch,
        provide_context=True
    )

    # Tasks for data extraction
    extract_walmart_task = PythonOperator(
        task_id='extract_walmart_data',
        python_callable=extract_data_from_kaggle,
        op_kwargs={'dataset': 'walmart'}
    )

    extract_instagram_task = PythonOperator(
        task_id='extract_instagram_data',
        python_callable=extract_data_from_kaggle,
        op_kwargs={'dataset': 'instagram'}
    )

    # Tasks for loading data into SQLite
    load_walmart_task = PythonOperator(
        task_id='load_walmart_to_sqlite',
        python_callable=load_to_sqlite,
        op_kwargs={'dataset': 'walmart'}
    )

    load_instagram_task = PythonOperator(
        task_id='load_instagram_to_sqlite',
        python_callable=load_to_sqlite,
        op_kwargs={'dataset': 'instagram'}
    )

    # Task dependencies
    choose_branch_task >> [extract_walmart_task, extract_instagram_task]
    extract_walmart_task >> load_walmart_task
    extract_instagram_task >> load_instagram_task

etl_with_branching = etl_with_branching()

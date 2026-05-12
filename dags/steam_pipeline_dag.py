from airflow.sdk import dag, task
from datetime import datetime, timedelta

from scripts.extract_steam import fetch_steam_data, save_raw_data, main
from scripts.transform_data import t_main
from scripts.load_to_sqlite import load_data

@dag(
    dag_id = "steam_pipeline_dag"
)

def steam_pipeline_dag():
    @task.python
    def extract():
        return main()
    
    @task.python
    def transform():
        return t_main()
    
    @task.python
    def load():
        return load_data()
    
    first = extract()
    second = transform()
    third = load()

    first>>second>>third
steam_pipeline_dag()
    

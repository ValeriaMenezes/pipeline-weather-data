from datetime import datetime, timedelta
from airflow.decorators import dag, task
from pathlib import Path
import sys, os
from dotenv import load_dotenv

# ensure project `src` directory is on PYTHONPATH before importing local modules
src_path = Path(__file__).resolve().parent.parent / 'src'
sys.path.insert(0, str(src_path))

env_path = Path(__file__).resolve().parent.parent / 'config/.env'
load_dotenv(env_path)

API_KEY = os.getenv('API_KEY')
url = f'http://api.openweathermap.org/data/2.5/weather?q=São Paulo,BR&appid={API_KEY}'

@dag(
    dag_id='weather_pipeline',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
    },
    description='Pipeline ETL Weather',
    schedule='0 */1 * * *',
    start_date=datetime(2026, 3, 12),
    catchup=False,
    tags=['weather', 'ETL', 'airflow']
)

def weather_pipeline():

    @task
    def extract():
        from extract_data import extract_weather_data
        return extract_weather_data(url)

    @task
    def transform():
        from transform_data import data_transformations
        df = data_transformations()
        df.to_parquet('/opt/airflow/data/temp_data.parquet', index=False)

    @task
    def load(): 
        import pandas as pd
        from load_data import load_weather_data
        df = pd.read_parquet('/opt/airflow/data/temp_data.parquet')
        load_weather_data('sp_weather', df)

    extract() >> transform() >> load()


weather_pipeline()
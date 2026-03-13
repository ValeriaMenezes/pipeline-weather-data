from src.extract_data import extract_data
from src.transform_data import data_transformations
from src.load_data import load_weather_data

import os
from pathlib import Path
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).resolve().parent.parent / 'config/.env'
load_dotenv(env_path)

API_KEY = os.getenv('API_KEY')

url = f'http://api.openweathermap.org/data/2.5/weather?q=São Paulo,BR&appid={API_KEY}'
table_name = 'sp_weather'

def pipeline():
    try:
        logging.info("Starting EXTRACT phase...")
        extract_weather_data(url)

        logging.info("Starting TRANSFORM phase...")
        df = data_transformations()

        logging.info("Starting LOAD phase...")
        load_weather_data(table_name, df)

        print("Pipeline executed successfully.")

    except Exception as e:
        logging.error(f"An error occurred during pipeline execution: {e}")
        import traceback
        traceback.print_exc()


pipeline()

# etl.py
import os
import pandas as pd
from sqlalchemy import create_engine
from extract import fetch_covid_data
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def etl_process():
    data = fetch_covid_data()
    if data:
        df = pd.DataFrame(data)
        # Select relevant columns
        df = df[['country', 'cases', 'todayCases', 'deaths', 'todayDeaths', 'recovered']]
        # Rename columns for clarity
        df.rename(columns={
            'country': 'Country',
            'cases': 'Total Cases',
            'todayCases': 'Today Cases',
            'deaths': 'Total Deaths',
            'todayDeaths': 'Today Deaths',
            'recovered': 'Recovered'
        }, inplace=True)
        
        # Retrieve database credentials from environment variables
        db_user = os.getenv('active')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'covid_db')

        # Create the database engine
        engine = create_engine(f'postgresql://{db_user}@{db_host}:{db_port}/{db_name}')
        
        # Load data into PostgreSQL
        try:
            df.to_sql('covid_stats', engine, if_exists='replace', index=False)
            print("Data loaded successfully.")
        except Exception as e:
            print(f"Error loading data to database: {e}")
    else:
        print("Failed to fetch data.")

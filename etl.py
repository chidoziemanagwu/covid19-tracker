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
        df.rename(columns={
            'country': 'Country',
            'cases': 'Total Cases',
            'todayCases': 'Today Cases',
            'deaths': 'Total Deaths',
            'todayDeaths': 'Today Deaths',
            'recovered': 'Recovered'
        }, inplace=True)

        # Render PostgreSQL URL
        db_url = os.getenv('DATABASE_URL', 'postgresql://user:LFz8hgVJji8FIJFy7n1I2gFNJKaJDSCu@dpg-crsltie8ii6s73eeob80-a.oregon-postgres.render.com/dbname_u7r1')

        # Create the database engine
        engine = create_engine(db_url)
        
        # Load data into PostgreSQL
        try:
            df.to_sql('covid_stats', engine, if_exists='replace', index=False)
            print("Data loaded successfully.")
        except Exception as e:
            print(f"Error loading data to database: {e}")
    else:
        print("Failed to fetch data.")

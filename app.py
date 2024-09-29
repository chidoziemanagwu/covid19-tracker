# app.py
from flask import Flask, render_template, redirect, url_for, flash
from sqlalchemy import create_engine
import pandas as pd
from etl import etl_process
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key')  # Needed for flashing messages

def get_data():
        # Retrieve database credentials from environment variables
    db_user = os.getenv('active')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'covid_db')

    # Create the database engine
    engine = create_engine(f'postgresql://{db_user}@{db_host}:{db_port}/{db_name}')
    query = "SELECT * FROM covid_stats"
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"Error fetching data from database: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

@app.route('/')
def home():
    df = get_data()
    if df.empty:
        tables = []
        titles = []
    else:
        tables = [df.to_html(classes='data', index=False, border=0)]
        titles = df.columns.values
    return render_template('index.html', tables=tables, titles=titles)

@app.route('/update', methods=['POST'])
def update():
    etl_process()
    flash('Data updated successfully!', 'success')
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

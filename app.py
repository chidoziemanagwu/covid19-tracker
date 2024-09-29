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
    # Retrieve Render PostgreSQL URL from environment variable
    db_url = os.getenv('DATABASE_URL', 'postgresql://user:LFz8hgVJji8FIJFy7n1I2gFNJKaJDSCu@dpg-crsltie8ii6s73eeob80-a.oregon-postgres.render.com/dbname_u7r1')
    
    # Create the database engine
    engine = create_engine(db_url)
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

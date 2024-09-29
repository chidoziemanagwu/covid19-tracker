# extract.py
import requests

def fetch_covid_data():
    url = "https://disease.sh/v3/covid-19/countries"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

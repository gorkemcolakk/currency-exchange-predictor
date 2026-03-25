import requests
import pandas as pd
from datetime import datetime, timedelta

def test_frankfurter_current():
    url = "https://api.frankfurter.app/latest?from=USD&to=TRY"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("USD/TRY Current:", data['rates']['TRY'])
        return True
    else:
        print(f"Frankfurter current failed ( {url} ):", response.status_code)
        return False

def test_frankfurter_historical():
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    url = f"https://api.frankfurter.app/{start_date}..{end_date}?from=USD&to=TRY"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        rates = data['rates']
        df = pd.DataFrame.from_dict(rates, orient='index', columns=['TRY'])
        df.index = pd.to_datetime(df.index)
        print("Historical head:")
        print(df.head())
        return True
    else:
        print("Frankfurter historical failed:", response.status_code)
        return False

if __name__ == "__main__":
    if test_frankfurter_current():
        test_frankfurter_historical()

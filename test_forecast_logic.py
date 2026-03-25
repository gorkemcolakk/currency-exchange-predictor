import requests
from datetime import datetime, timedelta
import pandas as pd

def test_forecast_data(currency):
    try:
        base = currency[:3].upper()
        start_date = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        
        url = f"https://api.frankfurter.app/{start_date}..{end_date}?from={base}&to=TRY"
        print(f"Testing URL: {url}")
        response = requests.get(url, timeout=20)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data_json = response.json()
            rates = data_json.get('rates', {})
            print(f"Number of days returned: {len(rates)}")
            if len(rates) > 0:
                print("First data point:", list(rates.items())[0])
            return True
        else:
            print("Response text:", response.text)
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

test_forecast_data("EURTRY=X")
test_forecast_data("USDTRY=X")

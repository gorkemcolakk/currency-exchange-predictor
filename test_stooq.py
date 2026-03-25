import pandas_datareader.data as web
from datetime import datetime, timedelta

try:
    print("Testing Stooq for USD/TRY...")
    start = datetime.now() - timedelta(days=365)
    end = datetime.now()
    df = web.DataReader('USDTRY', 'stooq', start, end)
    print("Columns:", df.columns)
    print("Head:")
    print(df.head())
except Exception as e:
    print("Stooq failed:", e)

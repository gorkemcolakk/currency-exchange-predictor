import yfinance as yf
import pandas as pd
from datetime import datetime

SUPPORTED_CURRENCIES = ["USDTRY=X", "EURTRY=X", "GBPTRY=X"]

for currency in SUPPORTED_CURRENCIES:
    print(f"Testing {currency}...")
    try:
        data = yf.download(currency, period='2d', interval='1d')
        print("Data columns:", data.columns)
        print("Data shape:", data.shape)
        if not data.empty:
            print("Latest rows:")
            print(data.tail())
            latest = data.iloc[-1]
            # Handle multi-index if present
            if isinstance(latest['Close'], pd.Series):
                current_close = float(latest['Close'].iloc[0])
            else:
                current_close = float(latest['Close'])
            print(f"Current close: {current_close}")
        else:
            print("Data is empty!")
    except Exception as e:
        print(f"Error ({currency}): {e}")
    print("-" * 20)

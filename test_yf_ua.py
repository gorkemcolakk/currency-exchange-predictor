import yfinance as yf
import requests

def test_yf_with_ua():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        print("Testing yfinance with custom User-Agent...")
        ticker = yf.Ticker("USDTRY=X", session=session)
        data = ticker.history(period="1mo")
        if not data.empty:
            print("Success! Data received:")
            print(data.tail())
            return True
        else:
            print("Still empty data.")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

test_yf_with_ua()

import requests, time
h = {'User-Agent': 'Mozilla/5.0'}
for s in ['USDTRY=X', 'EURTRY=X', 'GBPTRY=X']:
    res = requests.get(f'https://query2.finance.yahoo.com/v8/finance/chart/{s}?range=1d&interval=1m', headers=h).json()
    meta = res['chart']['result'][0]['meta']
    ts = meta.get('regularMarketTime', 0)
    print(f"{s}: {meta['regularMarketPrice']} (Updated: {time.ctime(ts)})")

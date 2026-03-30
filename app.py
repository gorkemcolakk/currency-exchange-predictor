import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, jsonify
from prophet import Prophet
import plotly.graph_objects as go
import json

app = Flask(__name__)

# Supported Currencies Settings
SUPPORTED_CURRENCIES = {
    "USDTRY=X": {"name": "Dolar", "flag": "us", "symbol": "$"},
    "EURTRY=X": {"name": "Euro", "flag": "eu", "symbol": "€"},
    "GBPTRY=X": {"name": "Sterlin", "flag": "gb", "symbol": "£"},
}

# Cache Settings
CACHE_DIR = "static/cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR, exist_ok=True)

def get_current_data_all():
    """Tüm güncel kur verilerini Yahoo üzerinden çeker (Tam tutarlılık için)."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    data = []
    for symbol, info in SUPPORTED_CURRENCIES.items():
        base = symbol[:3].upper()
        try:
            # 1 günlük veriyi 1 dakikalık aralıkla çekerek en son kur değerini alıyoruz
            url = f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?range=1d&interval=1m"
            res = requests.get(url, headers=headers, timeout=5).json()
            meta = res['chart']['result'][0]['meta']
            rate_val = meta['regularMarketPrice']
            prev_close = meta.get('previousClose', rate_val)
            change = rate_val - prev_close
            change_percent = (change / prev_close) * 100 if prev_close != 0 else 0
        except Exception as e:
            print(f"Yahoo live rate error for {symbol}: {e}")
            rate_val = 0.0
            change = 0.0
            change_percent = 0.0
            
        data.append({
            "symbol": symbol,
            "base": base,
            "name": info["name"],
            "rate": round(rate_val, 4),
            "change": round(change, 4),
            "change_percent": round(change_percent, 2),
            "flag": info["flag"],
            "currency_symbol": info["symbol"],
            "update_time": datetime.now().strftime('%H:%M:%S')
        })
    return data

def train_and_forecast(currency_symbol, periods=730):
    """Borsa verilerini çekerek gelişmiş Prophet tahmini üretir."""
    try:
        # 1. Veri Çekme (query2.finance.yahoo.com üzerinden direkt requests ile)
        # yfinance bazen rate limit yiyebiliyor, direkt requests daha sağlam.
        url = f"https://query2.finance.yahoo.com/v8/finance/chart/{currency_symbol}?range=5y&interval=1d"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        res = requests.get(url, headers=headers, timeout=15).json()
        
        if 'chart' not in res or res['chart']['result'] is None:
            print(f"Yahoo API Error: {res}")
            return None
            
        result_data = res['chart']['result'][0]
        timestamps = result_data['timestamp']
        closes = result_data['indicators']['quote'][0]['close']
        
        df = pd.DataFrame({
            'ds': [datetime.fromtimestamp(t) for t in timestamps], 
            'y': closes
        }).dropna()
        
        if df.empty:
            return None
        
        # 2. Model Kurulumu
        from prophet.make_holidays import make_holidays_df
        current_year = datetime.now().year
        tr_holidays = make_holidays_df(year_list=[current_year + i for i in range(-5, 4)], country='TR')
        
        model = Prophet(
            growth='linear',
            holidays=tr_holidays,
            yearly_seasonality=True,
            weekly_seasonality=False, 
            daily_seasonality=False,
            # Stabil bir trend tahmini için daha da optimize edildi
            changepoint_prior_scale=0.015,
            # Güven aralığı genişliği %50'ye düşürülerek çok daha dar bir bant sağlandı
            interval_width=0.5
        )
        model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
        
        # 3. Eğitim ve Tahmin
        model.fit(df)
        
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)
        
        # Sadece gerekli sütunlar
        result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
        
        # 4. Kayıt ve Grafik
        safe_name = currency_symbol.replace('=', '')
        csv_path = os.path.join(CACHE_DIR, f"{safe_name}_forecast.csv")
        result.to_csv(csv_path, index=False)
        
        # Plotly Grafiği (Modern Stil) - İki dilde de oluşturuyoruz
        langs = {
            'tr': {'actual': 'Gerçek Veri', 'forecast': 'Trend Tahmini', 'range': 'Tahmin Aralığı'},
            'en': {'actual': 'Actual Data', 'forecast': 'Trend Forecast', 'range': 'Forecast Range'}
        }
        
        for lang_code, labels in langs.items():
            fig = go.Figure()
            
            # Geçmiş Veri (Last 1 year for cleaner plot)
            df_plot = df[df['ds'] > (datetime.now() - timedelta(days=365))]
            fig.add_trace(go.Scatter(
                x=df_plot['ds'], y=df_plot['y'],
                name=labels['actual'],
                line=dict(color='#3b82f6', width=2)
            ))
            
            # Tahmin Verisi
            fig.add_trace(go.Scatter(
                x=result['ds'], y=result['yhat'],
                name=labels['forecast'],
                line=dict(color='#10b981', width=3, dash='dash')
            ))
            
            # Güven Aralığı
            x_fill = result['ds'].tolist() + result['ds'].tolist()[::-1]
            y_fill = result['yhat_upper'].tolist() + result['yhat_lower'].tolist()[::-1]
            
            fig.add_trace(go.Scatter(
                x=x_fill,
                y=y_fill,
                fill='toself',
                fillcolor='rgba(16, 185, 129, 0.1)',
                line=dict(color='rgba(255,255,255,0)'),
                hoverinfo="skip",
                showlegend=False,
                name=labels['range']
            ))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#f8fafc', family='Inter'),
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False),
                margin=dict(l=0, r=0, t=20, b=80),
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.15,
                    xanchor="center",
                    x=0.5
                )
            )
            
            plot_path = os.path.join(CACHE_DIR, f"{safe_name}_plot_{lang_code}.html")
            fig.write_html(plot_path, full_html=False, include_plotlyjs='cdn')
        
        return result
    except Exception as e:
        print(f"Forecast error for {currency_symbol}: {e}")
        return None

@app.route('/')
def index():
    try:
        forex_data = get_current_data_all()
    except Exception as e:
        print(f"Error in index: {e}")
        forex_data = []
    return render_template('index.html', forex_data=forex_data)

@app.route('/currency/<symbol>')
def currency_page(symbol):
    if symbol not in SUPPORTED_CURRENCIES:
        return redirect(url_for('index'))
    
    info = SUPPORTED_CURRENCIES[symbol]
    safe_name = symbol.replace('=', '')
    csv_path = os.path.join(CACHE_DIR, f"{safe_name}_forecast.csv")
    
    plot_path = os.path.join(CACHE_DIR, f"{safe_name}_plot.html")
    data = None
    
    # Cache kontrolü: Hem CSV hem de Grafik dosyası var mı bak
    if os.path.exists(csv_path) and os.path.exists(plot_path):
        mtime = os.path.getmtime(csv_path)
        # 2 saatten yeniyse cache kullan
        if datetime.now().timestamp() - mtime < 7200:
            try:
                data = pd.read_csv(csv_path)
                data['ds'] = pd.to_datetime(data['ds'])
            except:
                data = None
            
    if data is None or not os.path.exists(os.path.join(CACHE_DIR, f"{safe_name}_plot_tr.html")):
        data = train_and_forecast(symbol)
        if data is None:
             # Eğer download başarısız olduysa ama dosya varsa yine de eski dosyayı kullan
             if os.path.exists(csv_path):
                 data = pd.read_csv(csv_path)
                 data['ds'] = pd.to_datetime(data['ds'])

    if data is None:
        return "Veri alınamadı, borsa sunucuları yanıt vermiyor olabilir. Lütfen daha sonra tekrar deneyiniz."

    # Güncel veri listesinden ilgili kuru bul
    all_rates = get_current_data_all()
    current_item = next((item for item in all_rates if item['symbol'] == symbol), None)
    
    current_rate = current_item['rate'] if current_item else 0.0
    change_val = current_item['change'] if current_item else 0.0
    change_pct = current_item['change_percent'] if current_item else 0.0
    
    # Try logic to get rate
    try:
        current_rate = float(current_item['rate']) if current_item else float(data[data['ds'] <= datetime.now()]['yhat'].iloc[-1])
    except:
        current_rate = 0.0

    def get_forecast_val(days):
        target_date = datetime.now() + timedelta(days=days)
        # En yakın tahmini bul
        diffs = (data['ds'] - target_date).abs()
        idx = diffs.idxmin()
        val = float(data.loc[idx, 'yhat'])
        date_en = data.loc[idx, 'ds'].strftime('%B %Y')
        date_tr = date_en
        # Türkçe ay isimleri için basit bir haritalama (Locale ile uğraşmamak için)
        months = {
            "January": "Ocak", "February": "Şubat", "March": "Mart", "April": "Nisan",
            "May": "Mayıs", "June": "Haziran", "July": "Temmuz", "August": "Ağustos",
            "September": "Eylül", "October": "Ekim", "November": "Kasım", "December": "Aralık"
        }
        for en, tr in months.items():
            date_tr = date_tr.replace(en, tr)
            
        change = ((val - current_rate) / current_rate) * 100 if current_rate != 0 else 0
        return {"val": round(val, 4), "change": round(change, 2), "date_tr": date_tr, "date_en": date_en}

    forecasts = {
        "1w": get_forecast_val(7),
        "1m": get_forecast_val(30),
        "6m": get_forecast_val(180),
        "1y": get_forecast_val(365),
        "2y": get_forecast_val(730)
    }

    # 2 Yıllık Aylık Tahmin Listesi (Her ayın 1'i veya en yakını)
    monthly_targets = pd.date_range(start=datetime.now(), periods=25, freq='MS')
    monthly_data = []
    for target in monthly_targets:
        # En yakın tarihi bul
        diffs = (data['ds'] - target).abs()
        idx = diffs.idxmin()
        row = data.loc[idx].to_dict()
        monthly_data.append(row)
    
    table_list = monthly_data

    plot_file_tr = f"cache/{safe_name}_plot_tr.html"
    plot_file_en = f"cache/{safe_name}_plot_en.html"
    plot_exists = os.path.exists(os.path.join(CACHE_DIR, f"{safe_name}_plot_tr.html"))

    return render_template('currency.html', 
                         info=info, 
                         symbol=symbol,
                         current_rate=f"{current_rate:.4f}",
                         change_val=f"{change_val:+.4f}",
                         change_pct=f"{change_pct:+.2f}",
                         forecasts=forecasts,
                         table_list=table_list,
                         plot_file_tr=plot_file_tr,
                         plot_file_en=plot_file_en,
                         plot_exists=plot_exists,
                         update_time=current_item['update_time'] if current_item else datetime.now().strftime('%H:%M:%S'))

@app.route('/api/rates')
def api_rates():
    return jsonify(get_current_data_all())

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Burada mail gönderme veya db kaydı eklenebilir
        return render_template('contact.html', success=True)
    return render_template('contact.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))

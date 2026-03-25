from prophet import Prophet
from prophet.make_holidays import make_holidays_df
import numpy as np

def train_model(data):
    
    data = data[(data['Date'] >= '2020-01-01') & (data['Date'] <= '2022-12-31')]
    df = data[['Date', 'Close']]
    df.columns = ['ds', 'y']

    
    üst_sınır = df['y'].max() * 1.2
    df['cap'] = üst_sınır

   
    turkey_holidays = make_holidays_df(year_list=[2023, 2024, 2025, 2026], country='TR')

   
    model = Prophet(growth='logistic', holidays=turkey_holidays, changepoint_prior_scale=0.1)
    model.add_seasonality(name='yearly', period=365, fourier_order=10)
    model.add_seasonality(name='quarterly', period=90, fourier_order=5)
    model.fit(df)

    return model

def make_forecast(model, periods=730):
    
    future = model.make_future_dataframe(periods=periods)
    future['cap'] = model.history['cap'].iloc[0]
    forecast = model.predict(future)

    
    forecast[['yhat', 'yhat_lower', 'yhat_upper']] = forecast[['yhat', 'yhat_lower', 'yhat_upper']].round(4)

   
    forecast = forecast[forecast['ds'] <= '2026-12-31']

    return forecast
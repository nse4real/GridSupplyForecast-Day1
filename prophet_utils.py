# prophet_utils.py

import pandas as pd
from prophet import Prophet

def train_and_forecast(csv_path, periods=48):
    """
    Load a CSV with a 'Timestamp' column and an 'Import' column,
    resample it to hourly averages, fit a Prophet model (with UK holidays),
    and return a forecast for the next `periods` hours.
    """
    # 1. Load & rename
    df = pd.read_csv(csv_path, parse_dates=["Timestamp"])
    df = df.rename(columns={"Timestamp": "ds", "Import": "y"}).dropna()

    # 2. Resample to hourly ('1h'), avoiding the deprecation warning
    df = df.set_index("ds").resample("1h").mean().reset_index()

    # 3. Initialize & fit Prophet
    model = Prophet(daily_seasonality=True, weekly_seasonality=True)
    model.add_country_holidays(country_name="UK")
    model.fit(df)
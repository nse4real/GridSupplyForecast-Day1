# day3_evaluate.py

import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# 📌 1. Load and prepare the data
df = pd.read_csv("bishops-wood_wmids.csv", parse_dates=["Timestamp"])
df = df.rename(columns={"Timestamp": "ds", "Import": "y"}).dropna()

# Resample to **hourly** frequency using 'h' (not 'H') to avoid deprecation warnings
df = df.set_index("ds").resample("1h").mean().reset_index()

print(f"✅ Total rows after resampling: {len(df)}")

# 📊 2. Split into train/test using an 80/20 split
split_idx = int(len(df) * 0.8)
train, test = df.iloc[:split_idx], df.iloc[split_idx:]

print(f"↪ Training rows: {len(train)}, Testing rows: {len(test)}")

# 🔧 3. Fit Prophet model with UK holidays
model = Prophet(daily_seasonality=True, weekly_seasonality=True)
model.add_country_holidays(country_name="UK")
model.fit(train)

# 🧭 4. Forecast for the test set length
future = model.make_future_dataframe(periods=len(test), freq="h")
forecast = model.predict(future)

# 🎯 5. Compare predictions with ground truth
y_true = test["y"].values
y_pred = forecast["yhat"].tail(len(test)).values

mae = mean_absolute_error(y_true, y_pred)
rmse = np.sqrt(mean_squared_error(y_true, y_pred))

print(f"\n📈 Model Performance:")
print(f"   • MAE:  {mae:.2f}")
print(f"   • RMSE: {rmse:.2f}")
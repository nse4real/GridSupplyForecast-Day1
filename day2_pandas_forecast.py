# day2_pandas_forecast.py
import os
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error

# 1) Point to one CSV
csv_filename = "bishops-wood_wmids.csv"
if not os.path.exists(csv_filename):
    raise FileNotFoundError(f"'{csv_filename}' not found in {os.getcwd()}")

# 2) Load into pandas
df = pd.read_csv(csv_filename, parse_dates=["Timestamp"])

# 3) Quick EDA printout
print("=== Data Info ===")
print(df.info(), "\n")
print("=== First 5 Rows ===")
print(df.head(), "\n")
print("=== Missing Values ===")
print(df.isnull().sum(), "\n")

# 4) Prepare for Prophet
#    Prophet expects columns: ds (timestamp) and y (value)
column = "Import" if "Import" in df.columns else "Demand"
prophet_df = df[["Timestamp", column]].rename(columns={"Timestamp": "ds", column: "y"}).dropna()

# 5) Train/validation split (last 7 days as hold-out)
prophet_df = prophet_df.sort_values("ds")
cutoff = prophet_df["ds"].max() - pd.Timedelta(hours=1)
train_df = prophet_df[prophet_df["ds"] <= cutoff]
val_df   = prophet_df[prophet_df["ds"] >  cutoff]

print(f"Training on {len(train_df)} rows; validating on {len(val_df)} rows")

# 6) Fit Prophet model
model = Prophet(daily_seasonality=True, weekly_seasonality=True)
model.fit(train_df)

# 7) Forecast for the full period (train + validation)
future = model.make_future_dataframe(periods=len(val_df), freq="5min")
forecast = model.predict(future)

# 8) Evaluate on hold-out
#    Align forecast yhat to the validation period
pred = forecast.set_index("ds")["yhat"].loc[val_df["ds"]]
mae = mean_absolute_error(val_df["y"], pred)
rmse = mean_squared_error(val_df["y"], pred) ** 0.5
print(f"Validation MAE: {mae:.2f}, RMSE: {rmse:.2f}")

# 9) Plot results
plt.figure(figsize=(12, 6))
plt.plot(train_df["ds"], train_df["y"], label="Train")
plt.plot(val_df["ds"],   val_df["y"],   label="Actual (val)")
plt.plot(pred.index,     pred.values,  label="Forecast")
plt.legend()
plt.title(f"{csv_filename}: Actual vs Forecast (hold-out)")
plt.xlabel("Timestamp")
plt.ylabel(column)
plt.tight_layout()

# ✨ NEW: save to images folder
output_path = "images/day2_baseline_plot.png"
plt.savefig(output_path, dpi=150)    # dpi=150 gives a crisp image
print(f"Saved plot to {output_path}")


plt.show()
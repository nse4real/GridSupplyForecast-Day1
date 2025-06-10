from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("bishops-wood_wmids.csv", parse_dates=["Timestamp"])
df = df.rename(columns={"Timestamp":"ds","Import":"y"}).dropna()
df = df.set_index("ds").resample("1H").mean().reset_index()

model = Prophet(daily_seasonality=True, weekly_seasonality=True)
model.add_country_holidays(country_name='UK')
model.fit(df)

future = model.make_future_dataframe(periods=48, freq='H')
forecast = model.predict(future)

model.plot(forecast)
plt.title("Forecast - Bishops-Wood Import")
plt.show()

model.plot_components(forecast)
plt.show()
# eda_pandas.py
import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------------
# 1) Point to one CSV in this folder.
#    Note: Your CSV names have hyphens, so use the exact filename below.
# -------------------------------
csv_filename = "bishops-wood_wmids.csv"

# Check that the file actually exists in the current directory:
if not os.path.exists(csv_filename):
    raise FileNotFoundError(f"Cannot find '{csv_filename}' in {os.getcwd()}")

# -------------------------------
# 2) Load the CSV into pandas.
#    (Assumes there is a 'Timestamp' column to parse. If it's called something else,
#     adjust parse_dates accordingly.)
# -------------------------------
df = pd.read_csv(csv_filename, parse_dates=["Timestamp"])

# -------------------------------
# 3) Print basic info:
# -------------------------------
print("===== Data Info =====")
print(df.info(), "\n")         # columns, dtypes, non-null counts
print("===== First 5 rows =====")
print(df.head(), "\n")
print("===== Missing Values per Column =====")
print(df.isnull().sum(), "\n")

# -------------------------------
# 4) Plot a quick time‐series:
#    We’ll plot either the 'Import' column (if present) or 'Demand' otherwise.
# -------------------------------
column_to_plot = "Import" if "Import" in df.columns else "Demand"
print(f"Plotting hourly‐averaged '{column_to_plot}' from '{csv_filename}'...")

# Make sure 'Timestamp' is set as index for resampling:
df.set_index("Timestamp", inplace=True)

# Resample to hourly average and plot:
hourly = df[column_to_plot].resample("1H").mean()
plt.figure(figsize=(10, 5))
hourly.plot()
plt.title(f"Hourly Average of '{column_to_plot}' for {csv_filename}")
plt.xlabel("Timestamp")
plt.ylabel(column_to_plot)
plt.tight_layout()
plt.show()
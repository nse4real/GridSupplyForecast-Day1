# eda_multiple_gsps.py
import glob
import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------------
# 1) Find all files ending in "_wmids.csv" in the current folder
# -------------------------------
pattern = "*_wmids.csv"
file_list = glob.glob(pattern)
if not file_list:
    raise FileNotFoundError(f"No files matching '{pattern}' in {os.getcwd()}")

# -------------------------------
# 2) Loop through each CSV and print some basic info
# -------------------------------
for file_path in file_list:
    gsp_name = os.path.basename(file_path).replace("_wmids.csv", "")
    print(f"\n==== GSP: {gsp_name} (file: {file_path}) ====")

    # Load into pandas (parsing the 'Timestamp' column)
    df = pd.read_csv(file_path, parse_dates=["Timestamp"])

    # Print basic info + first 3 rows
    print(df.info())
    print("\nFirst 3 rows:")
    print(df.head(3))

    # Print missing‐value counts
    print("\nMissing values per column:")
    print(df.isnull().sum())

    # -------------------------------
    # 3) A simple plot of the first 7 days (if you have at least 7 days of data)
    # -------------------------------
    column_to_plot = "Import" if "Import" in df.columns else "Demand"
    df.set_index("Timestamp", inplace=True)

    # If the CSV has at least 7 days worth of hourly‐resampled data, plot it
    # Otherwise, just plot whatever you have
    try:
        idx = df.index
        start = idx.min()
        end = start + pd.Timedelta(days=7)
        subset = df.loc[start:end, column_to_plot]
    except Exception:
        subset = df[column_to_plot]

    hourly = subset.resample("1H").mean()

    plt.figure(figsize=(8, 4))
    hourly.plot()
    plt.title(f"{gsp_name}: Hourly Avg of '{column_to_plot}' (first 7 days)")
    plt.xlabel("Timestamp")
    plt.ylabel(column_to_plot)
    plt.tight_layout()
    plt.show()

print("\n✅ Done processing all GSP files.")

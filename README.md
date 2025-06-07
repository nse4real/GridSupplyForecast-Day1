# Grid-Supply Forecast Optimizer (Day 1: Setup & EDA)

## Overview
This directory contains scripts and data for **Day 1** of the Grid-Supply Forecast Optimizer project:
- **Environment setup**: Python virtual environment (`venv312`)
- **Package installation**: PySpark, Prophet, SHAP, pandas, matplotlib
- **Exploratory Data Analysis**: Loading and plotting NGED Live GSP CSV data

## Project Structure
├── artifacts/ # (for future model outputs, Dockerfiles, etc.)
├── data/ # Place your GSP CSVs here (e.g., bishops-wood_wmids.csv)
├── eda_multiple_gsps.py # Loop over multiple GSP CSVs and plot
├── eda_pandas.py # Pandas-based EDA script
├── eda_spark.py # PySpark-based EDA script
├── requirements.txt # Locked package versions for pip
├── venv312/ # Python 3.12 virtual environment
└── README.md # This file

## How to Run
1. Open VS Code and ensure Python interpreter is set to `.\venv\Scripts\python.exe`.
2. In the VS Code terminal (with `(venv)` active), run:
   ```powershell
   pip install -r requirements.txt
   python eda_pandas.py
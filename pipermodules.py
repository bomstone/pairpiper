import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import statsmodels
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
from statsmodels.tsa.stattools import coint, adfuller
import matplotlib

def fetch_data(asset, dataset, startdate, enddate):
    df = pd.read_csv('fulldb.csv', index_col = 'date', parse_dates=True).append(pd.read_csv('livedb.csv', index_col = 'date', parse_dates=True))
    data = df.loc[startdate:enddate]
    pivot_table = data.pivot(columns='symbol',
                             values=dataset)
    filtered_data = pivot_table.filter(items=asset)
    return filtered_data

def zscore(series):
    return (series - series.mean()) / np.std(series)


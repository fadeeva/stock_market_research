import numpy as np
import pandas as pd

import yfinance as yf
import datetime as dt

from scipy.optimize import brute


class SMAVectorBacktester():
    def __init__(self, symbol, start, end, interval, SMA1, SMA2):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.interval = interval
        
        self.SMA1 = SMA1
        self.SMA2 = SMA2
        
        self.results = None
        
        self.get_data()
    
    def get_data(self):
#         data = yf.download(self.symbol, start=self.start, end=self.end, interval=self.interval, auto_adjust=True)
        data = pd.read_csv('../../../data/IBM_2002-01-01_2022-12-31_1d.csv', index_col=0, parse_dates=True)
        data = data['Close'].to_frame()
        data.rename(columns={'Close': 'price'}, inplace=True)
        
        data['return'] = np.log(data['price'] / data['price'].shift(1))
        data['SMA1'] = data['price'].rolling(self.SMA1).mean()
        data['SMA2'] = data['price'].rolling(self.SMA2).mean()
        
        self.data = data
    
    def run_strategy(self):
        data = self.data.copy().dropna()
        
        data['position'] = np.where(data['SMA1'] > data['SMA2'], 1, -1)
        data['strategy'] = data['position'].shift(1) * data['return']
        
        data.dropna(inplace=True)
        
        data['c_returns'] = data['return'].cumsum().apply(np.exp)
        data['c_strategy'] = data['strategy'].cumsum().apply(np.exp)
        
        self.results = data
        
        # gross performance
        aperf = data['c_strategy'].iloc[-1]
        # out / underperformance
        operf = aperf - data['c_returns'].iloc[-1]
        
        return round(aperf, 2), round(operf, 2)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
import os

import numpy as np
import pandas as pd

import yfinance as yf
import datetime as dt

from scipy.optimize import brute


DATA_STORAGE = '../../../data'

class SMAVectorBacktester():
    def __init__(self, SMA1, SMA2, data_info):
#         self.symbol = symbol
#         self.start = start
#         self.end = end
#         self.interval = interval
        self.data_info = data_info
        self.data = None
        
        self.SMA1 = SMA1
        self.SMA2 = SMA2
        
        self.results = None
        
        self.get_data()
    
    def get_data(self):
        self.data_prepare()

        self.data = self.data['Close'].to_frame()
        self.data.rename(columns={'Close': 'price'}, inplace=True)
        
        self.data['return'] = np.log(data['price'] / data['price'].shift(1))
    
    def get_data_from_yf(self):
        self.data = yf.download(
            data['symbol'],
            start=data['start'],
            end=data['end'],
            interval=data['interval'],
            
            auto_adjust=True,
            progress=False,
            show_errors=True
        )
    
    def get_data_from_csv(self):
        f = f'{DATA_STORAGE}/{self.data_info}'
        if os.path.isfile(f):
            self.data = pd.read_csv(f'{f}', index_col=0, parse_dates=True)
        
    def data_prepare(self):
        if type(self.data_info) is str and self.data_info[-3:]=='csv':
            self.get_data_from_csv()
    
    def run_strategy(self):
        data = self.data.copy().dropna()
        
        data['SMA1'] = data['price'].rolling(self.SMA1).mean()
        data['SMA2'] = data['price'].rolling(self.SMA2).mean()
        
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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
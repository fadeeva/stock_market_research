import pandas as pd
import numpy as np

import bs4 as bs


# 1 PART -------------------------------------------------

# grab data from wiki
response = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
soup = bs.BeautifulSoup(response.text)
table = soup.find('table', {'class': 'wikitable sortable'})

tickers = []
for row in table.findAll('tr')[1:]:
    ticker = row.findAll('td')[0].text.replace('\n', '')
    if '.' in ticker:
        ticker = ticker.replace('.', '-')
    tickers.append(ticker)

# save it as pickle 
with open('../../data/sp500tickers.pickle', 'wb') as f:
    pk.dump(tickers, f)


# 2 PART -------------------------------------------------

# get list of tickers from pickle
with open('../../data/sp500tickers.pickle', 'rb') as f:
    sp500 = pk.load(f)

# get token for alphavantage
with open('../../../../alphavantage_token.TXT', 'rb') as f:
    TOKEN = f.read().decode('utf-8')

# data = pd.read_csv('../../data/sp500_Company_Overview.csv', index_col=0)
data = pd.DataFrame(index=sp500)

for ticker in sp500: # works only if alphavantage token is paid, otherwise, divide into pieces of 25 tickers
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={TOKEN}'
    r = requests.get(url)
    data.loc[ticker] = r.json()

data.to_csv('../data/sp500_Company_Overview.csv')

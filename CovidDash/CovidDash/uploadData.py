import pandas as pd
from sqlalchemy import create_engine
import requests
import os
import io

list_of_cryptocurrencies = ['AAVEUSDT_d', 'ADABTC_d', 'ADAUSDT_d', 'AAVEUSDT_1h', 'ADABTC_1h', 'ADAUSDT_1h']

DATABASE_URL = os.environ['DATABASE_URL']
#DATABASE_URL = 'postgres://ewxyjxpjxsqthz:e56aeb73ecb3b32ce4732e693aebcd263fabd11971ef7953f29f0f1266468796@ec2-34-194-158-176.compute-1.amazonaws.com:5432/des1cplt5kis06'
DATABASE_URL = DATABASE_URL.replace('postgres', 'postgresql')

conn = create_engine(DATABASE_URL)

for currency in list_of_cryptocurrencies:
    url = f'https://www.cryptodatadownload.com/cdd/Binance_{currency}.csv'
    response = requests.get(url).content
    data = pd.read_csv(io.StringIO(response.decode('utf-8')), header=1)
    data.sort_values('unix', inplace=True)
    data.to_sql(currency.lower(), con=conn, if_exists='replace', index=False)
#%%

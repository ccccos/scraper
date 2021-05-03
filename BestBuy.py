import os
import collections
import requests
import code.scraper.data_process as DP
import pandas as pd

class BestBuy():
    def __init__(self):
        self.maxTry = 5
        self.dp = DP.DataBase(db='monitor.db')
        self.name = 'BestBuy'
        self.df = pd.DataFrame(columns={'product_name', 'sku', 'daily_min'})

    def reset(self):
        self.maxTry = 5
        
    def get_skulist(self):
        tmp_cursor = dp.get_skulist(self.name)
        self.df.append(tmp_cursor)
        
    def get_Price(self):
        __url = 'https://api.bestbuy.com/v1/products((search={}))?apiKey=UFtoIkXmy0E6BMn5ddG6CE5u&sort=regularPrice.asc&show=regularPrice&format=json'

        for sku in self.df['sku']:
            if self.maxTry > 0:
                try:
                    r = requests.get(__url.format(sku))
                    result = r.json()
                    df['daily_min'] = min(int(result['products']), df['daily_min'])
                except requests.RequestException as e:
                    print("Error: failed to request BestBuy page for sku {}: ".format(sku), e)
                    self.maxTry -=1
            else:
                print("Failiure Maxium Reached.")

    def insert_hourlydata(self, df):
        for i in range(len(df)):
            dp.update(df['daily_min'].iloc[i], df['sku'].iloc[i])

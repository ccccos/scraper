import os
import collections
import requests
import code.scraper.data_process as DP
import Notification_Sender
import pandas as pd

class BestBuy():
    def __init__(self):
        self.maxTry = 5
        self.dp = DP.DataBase(db='monitor.db')
        self.name = 'BestBuy'
        self.df = None

    def reset(self):
        self.maxTry = 5
        
    def get_skulist(self):
        self.df = pd.DataFrame(dp.get_skulist(self.name), columns={'product_name', 'sku', 'daily_min'})
        
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
            dp.update(df['daily_min'][i], df['sku'][i])
    
    def send_email(self, df):
        email = Notification_Sender(df)
        email.send_email()

if __name__ == '__main__':
    bb = BestBuy()

    bb.get_skulist()
    bb.get_Price()
    bb.send_email()
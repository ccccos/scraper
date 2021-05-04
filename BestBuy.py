import os
import collections
import requests
import data_process as DP
from notification_sender import Notification_Sender
import pandas as pd
import time
pd.set_option('chained_assignment', None)
class BestBuy():
    def __init__(self):
        self.maxTry = 5
        self.dp = DP.DataBase(db='monitor.db')
        self.name = 'BestBuy'
        self.df = None

    def reset(self):
        self.maxTry = 5
        

    def get_skulist(self):
        self.df = self.dp.get_skulist(self.name)


    def get_Price(self):
        __url = 'https://api.bestbuy.com/v1/products((search={}))?apiKey=UFtoIkXmy0E6BMn5ddG6CE5u&sort=regularPrice.asc&show=regularPrice,salePrice,onSale&format=json'

        for i in range(len(self.df)):
            if self.maxTry > 0:
                try:                    
                    sku = self.df['sku'].iloc[i]
                    r = requests.get(__url.format(sku))
                    result = r.json()
                    print('processing '+ str(sku))
                    if len(result['products']) == 0:
                        continue
                    else:
                        if result['products'][0]['onSale'] == True:
                            self.df['daily_min'].iloc[i] = min(result['products'][0]['salePrice'], self.df['daily_min'].iloc[i])
                        else:
                            self.df['daily_min'].iloc[i] = min(result['products'][0]['regularPrice'], self.df['daily_min'].iloc[i])
                    time.sleep(1)
                except requests.RequestException as e:
                    print("Error: failed to request BestBuy page for sku {}: ".format(sku), e)
                    self.maxTry -=1
            else:
                print("Failiure Maxium Reached.")

    def insert_hourlydata(self):
        for i in range(len(self.df)):
            self.dp.update(self.df['daily_min'][i], self.df['sku'][i])
    
    def send_email(self):
        email = Notification_Sender(self.df)
        email.send_email()

if __name__ == '__main__':
    bb = BestBuy()
    bb.get_skulist()
    bb.get_Price()
    bb.send_email()
    '''    __url = 'https://api.bestbuy.com/v1/products((search={}))?apiKey=UFtoIkXmy0E6BMn5ddG6CE5u&sort=regularPrice.asc&show=regularPrice&format=json'
    r = requests.get(__url.format(5119600))
    result = r.json()
    print(result)
    print(result['products'][0]['regularPrice'])
    print(type(result['products'][0]['regularPrice']))'''
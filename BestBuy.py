import requests
import data_process as DP
from notification_sender import Notification_Sender
import pandas as pd
import time
import datetime
pd.set_option('chained_assignment', None)
class BestBuy():
    def __init__(self):
        self.maxTry = 5
        self.dp = DP.DataBase(db='monitor.db')
        self.name = 'BestBuy'
        self.df = None
        self.date = datetime.datetime.now().strftime(r'%Y-%m-%d %H:%M:%S')
    def reset(self):
        self.maxTry = 5
        
    def update_date(self):
        self.date = datetime.datetime.today().strftime(r'%Y-%m-%d %H:%M:%S')

    def get_skulist(self):
        self.df = self.dp.get_skulist(self.name)


    def get_Price(self):
        __url = 'https://api.bestbuy.com/v1/products((search={}))?apiKey=UFtoIkXmy0E6BMn5ddG6CE5u&sort=regularPrice.asc&show=regularPrice,salePrice,onSale&format=json'

        for i in range(len(self.df)):
            self.update_date()
            if self.maxTry > 0:
                try:                    
                    sku = self.df['sku'].iloc[i]
                    r = requests.get(__url.format(sku))
                    result = r.json()
                    if len(result['products']) == 0:
                        continue
                    else:
                        if result['products'][0]['onSale'] == True:
                            if result['products'][0]['salePrice'] != self.df['daily_min'].iloc[i]:
                                self.df['daily_min'].iloc[i] = result['products'][0]['salePrice']
                                self.df['updated_on'].iloc[i] = self.date
                        else:
                            if result['products'][0]['regularPrice'] != self.df['daily_min'].iloc[i]:
                                self.df['daily_min'].iloc[i] = result['products'][0]['regularPrice']
                                self.df['updated_on'].iloc[i] = self.date
                    time.sleep(0.5)
                except requests.RequestException as e:
                    print("Error: failed to request BestBuy page for sku {}: ".format(sku), e)
                    self.maxTry -=1
            else:
                print("Failiure Maxium Reached.")
        self.df = self.df[pd.to_datetime(self.df['updated_on']) > (datetime.datetime.now() - datetime.timedelta(hours=1))]

    def insert_data(self):
        for i in range(len(self.df)):
            '''To use other Python types with SQLite, you must adapt them to one of the sqlite3 module’s supported types for SQLite: one of NoneType, int, float, str, bytes.'''
            self.dp.update(float(self.df['daily_min'].iloc[i]), self.df['updated_on'].iloc[i], self.name, int(self.df['sku'].iloc[i]))
    
    def send_email(self):
        email = Notification_Sender(self.name, self.df)
        email.send_email()

    def run(self):
        self.get_skulist()
        self.get_Price()
        self.insert_data()
        self.send_email()

if __name__ == '__main__':
    bb = BestBuy()
    bb.run()
    '''    __url = 'https://api.bestbuy.com/v1/products((search={}))?apiKey=UFtoIkXmy0E6BMn5ddG6CE5u&sort=regularPrice.asc&show=regularPrice&format=json'
    r = requests.get(__url.format(5119600))
    result = r.json()
    print(result)
    print(result['products'][0]['regularPrice'])
    print(type(result['products'][0]['regularPrice']))'''
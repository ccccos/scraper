import sqlite3
import datetime
import pandas as pd

'''This module functions are to connect to DB and inesrt new daily record'''
class DataBase():
    def __init__(self, db):
        self.date = datetime.datetime.now().strftime(r'%Y-%m-%d')
        self.df = pd.DataFrame(columns={'shop_name', 'price_data'})
        con = None
        try:
            con = sqlite3.connect(db)
        except sqlite3.Error as e:
            print('Connection failed: ', e)
        self.connection = con
        self.cursor = con.cursor()

    def get_skulist(self, shop_name) -> query_result:
        __get_query = 'SELECT product_name, sku, daily_min FROM sku_table WHERE shop=%s; '
        try:
            return self.cursor.execute(__get_query.format(shop_name)).fetchall()
        except sqlite3.Error as e:
            print("Fetch All Error: ", e)
            return None

    def update(self, price, sku):
        __insert_query = 'UPDATE sku_table SET daily_min = %s WHERE sku = %s'
        try:
            self.cursor.execute(__insert_query.format(price, sku))
        except sqlite3.Error as e:
            print("Insert Error: ", e)

    def insert_eod(self):
        __eod_query = 'SELECT DISTINCT shop FROM sku_table'
        __eod_query2 = 'SELECT product_name, sku, daily_min FROM sku_table WHERE shop = %s'
        try:
            shops = self.cursor.execute(__eod_query).fetchall()
            for shop in shops:
                new_df = pd.DataFrame(columns={'product_name', 'sku', 'daily_min'})
                result = self.cursor.execute(__eod_query2.format(shop))
                for row in result:
                    new_df.append(row)
        except sqlite3.Error as e:
            print("Get EOD Error: ", e)
            shops = None
        
    def create_table(self, create_query):
        try:
            self.cursor.execute(create_query)
        except sqlite3.Error as e:
            print("Create Table Error: ", e)
    

if __name__ == '__main__':
    db = DataBase('monitor.db')
    create_sku_table = ''' CREATE TABLE IF NOT EXISTS sku_table (
                            sku integer PRIMARY KEY,
                            shop text NOT NULL,        
                            daily_min integer,
                            product_name text   
                        ); '''
    create_history_table = '''CREATE TABLE IF NOT EXISTS history_table (
                                date text PRIMARY KEY,
                                shop_name text NOT NULL,
                                price_data text,
                                FOREIGN KEY (shop_name) REFERENCES sku_table (shop)
                        ); '''
    alter_sku = r' ALTER TABLE sku_table ADD product_name text; '

    #db.create_table(alter_sku)
    #db.create_table(create_history_table)
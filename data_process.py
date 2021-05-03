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

    def commit(self):
        self.connection.commit()

    def get_skulist(self, shop_name):
        __get_query = 'SELECT product_name, sku, daily_min FROM sku_table WHERE shop=?; '
        try:
            return self.cursor.execute(__get_query, shop_name).fetchall()
        except sqlite3.Error as e:
            print("Fetch All Error: ", e)
            return None

    def update(self, price, sku):
        __insert_query = 'UPDATE sku_table SET daily_min = ? WHERE sku = ?; '
        try:
            self.cursor.execute(__insert_query, (price, sku))
            self.commit()
        except sqlite3.Error as e:
            print("Insert Error: ", e)

    def insert_eod(self):
        __eod_query = 'SELECT DISTINCT shop FROM sku_table'
        __eod_query2 = 'SELECT sku, daily_min FROM sku_table WHERE shop = ?; '
        __dif_query = 'SELECT sku, price FROM history_table INNER JOIN sku_table ON history_table.sku = sku_table.sku WHERE ' ###TODO
        __insert_eod = 'INSERT INTO history_table VALUES (?, ?, ?);'
        try:
            shops = self.cursor.execute(__eod_query).fetchall()
            for shop in shops:
                result = self.cursor.execute(__eod_query2, (shop)).fetchall()
                new_df = pd.DataFrame(result, columns={'sku', 'daily_min'})
                for i in range(len(new_df)):
                    self.cursor.execute(__insert_eod, (new_df['sku'][i], datetime.today(), new_df['daily_min'][i]))
        except sqlite3.Error as e:
            print("Get EOD Error: ", e)
            shops = None
        
    def create_table(self, create_query):
        try:
            self.cursor.execute(create_query)
        except sqlite3.Error as e:
            print("Create Table Error: ", e)
    
    def insert(self, sku, shop, daily_min, product_name):
        self.cursor.execute('INSERT OR REPLACE INTO sku_table (sku, shop, daily_min, product_name) VALUES (?, ?, ?, ?)', (sku, shop, daily_min, product_name))
        self.commit()

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
    new_history_table = '''CREATE TABLE IF NOT EXISTS history_table (
                                sku integer,
                                date text,
                                price integer,
                                FOREIGN KEY (sku) REFERENCES sku_table (sku)
                        ); '''
    alter_sku = r' ALTER TABLE sku_table ADD product_name text; '

    #db.create_table(alter_sku)
    #db.create_table(create_history_table)

    df = pd.read_excel('new_monitor.xlsx')

    for i in range(len(df)):
        db.insert(int(df['sku'][i]), df['shop'][i], 0, df['product_name'][i])
import code.scraper.BestBuy as BB
import code.scraper.data_process as data
import code.scraper.notification_sender as ns


class Monitor():
    def __init__(self):
        self.db = data.DataBase('monitor.db')
        self.bb = BB.BestBuy()


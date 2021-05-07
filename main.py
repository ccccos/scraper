import BestBuy as BB
import data_process as data
import notification_sender as ns
import time

bb = BB.BestBuy()

while True:
    bb.run()
    time.sleep(3600)


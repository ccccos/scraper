import requests
import data_process as DP
from notification_sender import Notification_Sender
import pandas as pd
import time
import datetime
pd.set_option('chained_assignment', None)

import requests

import requests

url = "https://walmart2.p.rapidapi.com/productDetails"

querystring = {"usItemId":"706203065"}

headers = {
    'x-rapidapi-key': "ce606598e2msh366e8096bc4fa8cp126b5djsn0ba96cb215c5",
    'x-rapidapi-host': "walmart2.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
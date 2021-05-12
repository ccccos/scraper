import requests
import data_process as DP
from notification_sender import Notification_Sender
import pandas as pd
import time
import datetime
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
pd.set_option('chained_assignment', None)

options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.set_headless(True)

_url = 'https://brickseek.com/walmart-inventory-checker?sku={}'

xpath= '//*[@id="main"]/div/div[2]/div[2]/div[1]/div/div[1]/span'
popup = '/html/body/div[2]/div[1]/span'
bodytext = '//*[@id="main"]/div/div[2]/div[2]/h2'
email = '//*[@id="_form_609598B2AB650_"]/div[1]/i' 
driver = webdriver.Chrome('chromedriver.exe')
driver.get(_url.format(54310139))
driver.find_element_by_xpath(popup).click()
print('popup clicked')
driver.find_element_by_xpath(bodytext).click()
print('text clicked')
WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, email))).click()
print('email clicked')
p = driver.find_element_by_xpath(xpath)
print(p)
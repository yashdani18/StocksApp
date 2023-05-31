import math
import time

from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient

URL_MONGO = ''
client = MongoClient(URL_MONGO)
db = client['investment_manager']
collection = db['ticker_losers']
collection.drop()
time.sleep(1)
url = 'https://ticker.finology.in/market/top-losers'

response = requests.get(url).text
soup = BeautifulSoup(response, 'lxml')

companies = soup.find(id="mainContent_pnlhighlow").find('tbody').find_all('tr')
counter = 0
for company in companies:
    dataFields = company.find_all('td')
    name = dataFields[1].text
    url = dataFields[1].find('a')['href']
    ticker = url.split('/')[2]
    price = dataFields[2].text
    change = dataFields[3].text[:-1]
    if float(price) > 100 and math.fabs(float(change)) < 8:
        counter += 1
        dictionary = {
            'company': name,
            'ticker': ticker,
            'url': url,
            'price': float(price),
            'change': float("{:.2f}".format(float(change)))
        }

        print(dictionary)
        print(collection.insert_one(dictionary).acknowledged)
        # print(counter, dataFields[0].text, name, ticker, price, change)

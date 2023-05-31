import json

from pymongo import MongoClient

from constants import TICKER_KEYS
from get.data_from_ticker_bs4 import get_data_from_ticker_using_bs4

URL_MONGO = ''
client = MongoClient(URL_MONGO)
db = client['investment_manager']


def update_progress(index, companies):
    temp = ''
    for i, company in enumerate(companies):
        if i <= index:
            temp += '#'
        else:
            temp += "."
    return temp


def update_collection(collection_ticker, filename):
    f = open('../data/data_companies_' + filename + '.json')
    companies = json.load(f)['companies']
    print(f'Progress: {update_progress(-1, companies)} 0/{len(companies)}', end="")
    for index, company in enumerate(companies):
        ticker = company['symbol']
        dictionary = get_data_from_ticker_using_bs4(ticker)
        if dictionary is None:
            return

        if filename == 'portfolio':
            avg_price = company['avg_price']
            quantity = company['quantity']
            dictionary['avg_price'] = avg_price
            dictionary['quantity'] = quantity
            dictionary['invested_value'] = float("{:.2f}".format(avg_price * quantity))
            dictionary['current_value'] = float("{:.2f}".format(quantity * dictionary['Price']))
            dictionary['pl_value_absolute'] = float(dictionary['current_value'] - dictionary['invested_value'])
            dictionary['pl_value_percent'] = float(
                (dictionary['current_value'] - dictionary['invested_value']) / dictionary['invested_value'] * 100)
        if collection_ticker.find_one({'Ticker': dictionary[TICKER_KEYS.TICKER]}):
            if collection_ticker.replace_one({'Ticker': dictionary[TICKER_KEYS.TICKER]}, dictionary).acknowledged:
                # print(f'Document updated successfully: {ticker}')
                print(f'Progress: {update_progress(index, companies)} {index + 1}/{len(companies)}', end="")
            else:
                print('Document failed to update')
        else:
            if collection_ticker.insert_one(dictionary).acknowledged:
                # print(f'Document inserted successfully: {ticker}')
                print(f'Progress: {update_progress(index, companies)} {index + 1}/{len(companies)}', end="")
            else:
                print('Document failed to insert')
    print()


update_collection(db['ticker_portfolio'], 'portfolio')
# update_collection(db['ticker_watchlist'], 'watchlist')

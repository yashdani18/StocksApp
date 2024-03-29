from bs4 import BeautifulSoup
import requests
from constants import TICKER_KEYS
from pymongo import MongoClient

URL_MONGO = ''
client = MongoClient(URL_MONGO)
db = client['investment_manager']
collection_ticker = db['ticker']


def prepare_url(p_ticker):
    return 'https://ticker.finology.in/company/' + p_ticker


def get_html_from_ticker(p_url):
    t_response = requests.get(p_url).text
    # print(t_response)
    return t_response


def parse_html_from_ticker(p_ticker, p_response):
    t_dictionary = {}
    soup = BeautifulSoup(p_response, 'lxml')

    std_con_element = soup.find(id="mainContent_switchCon")
    if std_con_element is not None:
        # print('Consolidated Available')
        print('')
        if p_ticker[0] == '/':
            url = 'https://ticker.finology.in' + p_ticker + '?mode=C'
            ticker_manipulation = p_ticker.split('/')[2]
            print(ticker_manipulation)
            p_ticker = ticker_manipulation
        else:
            url = 'https://ticker.finology.in/company/' + p_ticker + '?mode=C'
        temp_response = requests.get(url).text
        soup = BeautifulSoup(temp_response, 'lxml')
    else:
        print('')
        # print('Consolidated not available')

    if p_ticker[0] == '/':
        p_ticker = p_ticker.split('/')[2]

    try:
        t_dictionary[TICKER_KEYS.NAME] = soup.find(id="mainContent_ltrlCompName").text.strip()
        t_dictionary[TICKER_KEYS.PRICE] = float(soup.find(class_="currprice").text.strip())
        t_dictionary[TICKER_KEYS.WEEK_52_HIGH] = float(soup.find(id="mainContent_ltrl52WH").text.strip())
        t_dictionary[TICKER_KEYS.WEEK_52_LOW] = float(soup.find(id="mainContent_ltrl52WL").text.strip())

        t_dictionary[TICKER_KEYS.SECTOR] = (soup.find(id="mainContent_compinfoId")).find('a').text.strip()
        t_dictionary[TICKER_KEYS.TICKER] = p_ticker

        t_dictionary[TICKER_KEYS.RATING_FINSTAR] = float(soup.find(id="mainContent_ltrlOverAllRating")['aria-label'][-11:-10])

        t_dictionary[TICKER_KEYS.RATING_OWNERSHIP_STATUS] = soup.find(id="mainContent_divOwner").find('span').text
        t_dictionary[TICKER_KEYS.RATING_OWNERSHIP_VALUE] = float(soup.find_all('div', id="mainContent_ManagementRating")[0]['aria-label'][-13:-10])

        t_dictionary[TICKER_KEYS.RATING_VALUATION_STATUS] = soup.find(id="mainContent_divValuation").find('span').text
        t_dictionary[TICKER_KEYS.RATING_VALUATION_VALUE] = float(soup.find_all('div', id="mainContent_ValuationRating")[0]['aria-label'][-13:-10])

        t_dictionary[TICKER_KEYS.RATING_EFFICIENCY_STATUS] = soup.find(id="mainContent_divEff").find('span').text
        t_dictionary[TICKER_KEYS.RATING_EFFICIENCY_VALUE] = float(soup.find_all('div', id="mainContent_EfficiencyRating")[0]['aria-label'][-13:-10])

        t_dictionary[TICKER_KEYS.RATING_FINANCIALS_STATUS] = soup.find(id="mainContent_divFinance").find('span').text
        t_dictionary[TICKER_KEYS.RATING_FINANCIALS_VALUE] = float(soup.find_all('div', id="mainContent_FinancialsRating")[0]['aria-label'][-13:-10])

        t_dictionary[TICKER_KEYS.MARKET_CAP] = float(soup.select('div.col-6.col-md-4.compess')[0].select('span.Number')[0].text.strip())
        t_dictionary[TICKER_KEYS.ENTERPRISE_VALUE] = float(soup.select('div.col-6.col-md-4.compess')[1].select('span.Number')[0].text.strip())

        t_dictionary[TICKER_KEYS.NUMBER_OF_SHARES] = float(soup.select('div.col-6.col-md-4.compess')[2].select('span.Number')[0].text.strip())

        t_dictionary[TICKER_KEYS.PE] = float(soup.select('div.col-6.col-md-4.compess')[3].select('p')[0].text.strip())
        t_dictionary[TICKER_KEYS.PB] = float(soup.select('div.col-6.col-md-4.compess')[4].select('p')[0].text.strip())
        t_dictionary[TICKER_KEYS.FV] = soup.select('div.col-6.col-md-4.compess')[5].select('p')[0].text.strip()

        t_dictionary[TICKER_KEYS.DIV_YIELD] = soup.select('div.col-6.col-md-4.compess')[6].select('p')[0].text.strip()
        t_dictionary[TICKER_KEYS.BOOK_VALUE] = float(soup.select('div.col-6.col-md-4.compess')[7].select('span.Number')[0].text.strip())

        try:
            t_dictionary[TICKER_KEYS.CASH_NII] = float(soup.select('div.col-6.col-md-4.compess')[8].select('span.Number')[0].text.strip())
        except:
            t_dictionary[TICKER_KEYS.CASH_NII] = 0

        try:
            t_dictionary[TICKER_KEYS.DEBT_CTI] = float(soup.select('div.col-6.col-md-4.compess')[9].select('span.Number')[0].text.strip())
        except:
            t_dictionary[TICKER_KEYS.DEBT_CTI] = 0

        t_dictionary[TICKER_KEYS.PROMOTER_HOLDING] = float(soup.select('div.col-6.col-md-4.compess')[10].select('p')[0].text.strip()[:-1])

        t_dictionary[TICKER_KEYS.EPS] = float(soup.select('div.col-6.col-md-4.compess')[11].select('span.Number')[0].text.strip())

        try:
            t_dictionary[TICKER_KEYS.SALES_CAR] = float(soup.select('div.col-6.col-md-4.compess')[12].select('p')[0].text.strip()) if (t_dictionary[TICKER_KEYS.SECTOR].strip())[:4] == 'Bank' else float(soup.select('div.col-6.col-md-4.compess')[12].select('span.Number')[0].text.strip())
        except:
            t_dictionary[TICKER_KEYS.SALES_CAR] = 0

        try:
            t_dictionary[TICKER_KEYS.ROE] = float(soup.select('div.col-6.col-md-4.compess')[13].select('span.Number')[0].text)
        except:
            t_dictionary[TICKER_KEYS.ROE] = 0

        try:
            t_dictionary[TICKER_KEYS.ROCE] = float(soup.select('div.col-6.col-md-4.compess')[14].select('span.Number')[0].text)
        except:
            t_dictionary[TICKER_KEYS.ROCE] = 0

        try:
            t_dictionary[TICKER_KEYS.PROFIT] = float(soup.select('div.col-6.col-md-4.compess')[15].select('span.Number')[0].text)
        except:
            t_dictionary[TICKER_KEYS.PROFIT] = 0

        t_dictionary[TICKER_KEYS.CARD4] = float("{:.2f}".format(float(soup.find_all(class_='card cardscreen cardsmall')[4].find_all('span')[-1].text.strip())))
        t_dictionary[TICKER_KEYS.CARD5] = float("{:.2f}".format(float(soup.find_all(class_='card cardscreen cardsmall')[5].find_all('span')[-1].text.strip())))
        t_dictionary[TICKER_KEYS.CARD6] = float("{:.2f}".format(float(soup.find_all(class_='card cardscreen cardsmall')[6].find_all('span')[-1].text.strip())))
        t_dictionary[TICKER_KEYS.CARD7] = float("{:.2f}".format(float(soup.find_all(class_='card cardscreen cardsmall')[7].find_all('span')[-1].text.strip())))

        t_dictionary[TICKER_KEYS.DIFF_52] = float(t_dictionary[TICKER_KEYS.WEEK_52_HIGH]) - float(t_dictionary[TICKER_KEYS.PRICE])
        t_dictionary[TICKER_KEYS.PERCENT_FROM_52_HIGH] = float("{:.2f}".format((float(t_dictionary[TICKER_KEYS.WEEK_52_HIGH]) - float(t_dictionary[TICKER_KEYS.PRICE])) / float(t_dictionary[TICKER_KEYS.WEEK_52_HIGH]) * 100))
        t_dictionary[TICKER_KEYS.PERCENT_FROM_52_LOW] = float("{:.2f}".format((float(t_dictionary[TICKER_KEYS.PRICE]) - float(t_dictionary[TICKER_KEYS.WEEK_52_LOW])) / float(t_dictionary[TICKER_KEYS.PRICE]) * 100))

    except:
        return None
    return t_dictionary


def get_data_from_ticker_using_bs4(p_ticker):
    if p_ticker[0] == '/':
        url = 'https://ticker.finology.in' + p_ticker
    else:
        url = prepare_url(p_ticker)
    response = get_html_from_ticker(url)
    dictionary = parse_html_from_ticker(p_ticker, response)
    # print(dictionary)
    return dictionary


# print(get_data_from_ticker_using_bs4('GPIL'))

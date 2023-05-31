import time

from constants.NEWS import URL_NEWS_GODREJ_CONSUMER_PRODUCTS, URL_NEWS_TATA_MOTORS

from pymongo import MongoClient

from news.NewsGodrejConsumerProducts import NewsGodrejConsumerProducts
from news.BatchNews import fetch_news_from_company
from news.NewsTataMotors import NewsTataMotors

URL_MONGO = ''
client = MongoClient(URL_MONGO)
db = client['investment_manager']
collection_news = db['news']
time.sleep(1)

ticker = 'TATAMOTORS'


def save_news_article_to_db(p_news_article):
    if collection_news.find_one({'headline': p_news_article['headline']}):
        print('headline found')
    else:
        print('Inserting document: ', collection_news.insert_one(p_news_article).acknowledged)
    # return collection_news.insert_one(p_news_article).acknowledged


# news_array = []
# news_array = get_news_from_happiest_minds()

news_array = fetch_news_from_company(NewsTataMotors())
# print(dictionary)
for news in news_array:
    news['ticker'] = ticker
    news['read'] = False

    save_news_article_to_db(news)

# print(news_array)


def get_news_articles_from_db(company_ticker):
    return collection_news.find({'ticker': company_ticker})


news_articles = get_news_articles_from_db(ticker)
read_articles = []
unread_articles = []
for news_article in news_articles:
    if news_article['read']:
        read_articles.append(news_article)
    else:
        unread_articles.append(news_article)


print('read articles', read_articles)
print('unread', unread_articles)


def mark_all_articles_as_read(company_ticker):
    news_articles = collection_news.find({'ticker': company_ticker, 'read': False})
    for i in news_articles:
        print(i['date'])
        print(collection_news.find_one_and_update({'ticker': company_ticker, 'date': i['date']}, {'$set': {'read': True}}))


# mark_all_articles_as_read('GODREJCP')


def delete_all_articles_from_company(ticker):
    collection_news.delete_many({'ticker': ticker})


# delete_all_articles_from_company('HAPPSTMNDS')



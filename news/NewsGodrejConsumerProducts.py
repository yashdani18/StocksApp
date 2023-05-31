import news.News
from constants.NEWS import URL_NEWS_GODREJ_CONSUMER_PRODUCTS
from news.News import News
from datetime import datetime


class NewsGodrejConsumerProducts(News):
    def __init__(self):
        self.url = URL_NEWS_GODREJ_CONSUMER_PRODUCTS
        super().__init__(self.url)

    def get_news(self):
        self.set_html()
        self.set_soup()

        cards = self.soup.find_all(class_="fwp file_downloaded")
        arr_news = []
        for card in cards:
            headline = card.find_all('a')[0].text.strip()
            date = card.find_all('p')[0].text.strip()
            dt_obj = datetime.strptime(date,
                                       '%d %B %Y')
            date_in_ms = dt_obj.timestamp() * 1000

            dict_news = news.News.get_dictionary(headline, date, date_in_ms)

            arr_news.append(dict_news)
        return arr_news


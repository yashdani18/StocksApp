import news.News
from news.News import News
from constants.NEWS import DICTIONARY_HEADLINE, DICTIONARY_DATE_STRING, DICTIONARY_DATE_MS, URL_NEWS_TATA_CONSUMER


class NewsTataConsumer(News):
    def __init__(self):
        self.url = URL_NEWS_TATA_CONSUMER
        super().__init__(self.url)

    def get_news(self):
        self.set_html()
        self.set_soup()
        list_items = self.soup.find(class_="views-infinite-scroll-content-wrapper").find('ul').find_all('li')

        arr_news = []

        for item in list_items:
            headline = item.find('a').text.strip()
            date_string = item.find(class_="card__date").text.strip()
            date_ms = news.News.get_date_in_ms(date_string, "%d %B %Y")

            dict_news = news.News.get_dictionary(headline, date_string, date_ms)

            arr_news.append(dict_news)
        return arr_news

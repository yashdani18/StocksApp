from datetime import datetime

from constants.NEWS import URL_NEWS_TVS_MOTORS
from news.News import News, get_dictionary


class NewsTVSMotors(News):
    def __init__(self):
        self.url = URL_NEWS_TVS_MOTORS
        super().__init__(self.url)

    def get_news(self):
        self.set_html()
        self.set_soup()

        cards = self.soup.find_all(class_="news-head-content")
        arr_news = []
        for card in cards:
            headline = card.find('h3').text.strip()
            date_string = card.find('p').text
            split_string = date_string.split('|')
            date_object = datetime.strptime(split_string[1].strip(), '%d %b %Y')
            date_ms = date_object.timestamp() * 1000

            news = get_dictionary(headline, date_string, date_ms)

            arr_news.append(news)
        return arr_news


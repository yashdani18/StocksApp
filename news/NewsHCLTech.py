from datetime import datetime

from constants.NEWS import URL_NEWS_HCL_TECH
from news.News import News, get_dictionary


class NewsHCLTech(News):
    def __init__(self):
        self.url = URL_NEWS_HCL_TECH
        super().__init__(self.url)

    def get_news(self):
        self.set_html()
        self.set_soup()

        cards = self.soup.find_all(class_='card')

        arr_news = []

        for card in cards:
            headline = card.find(class_="newsroom-title").text.strip()
            date_string = card.find(class_="newsroom-header").find_all('span')[1].text.strip()
            date_object = datetime.strptime(date_string, "%b %d, %Y")
            date_ms = date_object.timestamp() * 1000

            news = get_dictionary(headline, date_string, date_ms)

            arr_news.append(news)
        return arr_news

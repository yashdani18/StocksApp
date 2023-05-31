from datetime import datetime

from constants.NEWS import URL_NEWS_TATA_CONSULTANCY_SERVICES
from news.News import News, get_dictionary


class NewsTataConsultancyServices(News):
    def __init__(self):
        self.url = URL_NEWS_TATA_CONSULTANCY_SERVICES
        super().__init__(self.url)

    def get_news(self):
        self.set_html()
        self.set_soup()

        cards = self.soup.find_all(class_="filter-list-details position-relative")
        arr_news = []
        for card in cards:
            headline = card.find(class_="filter-details-title").text
            date_string = card.find(class_="filter-details-type-data").find_all('span')[2].text
            date_object = datetime.strptime(date_string, "%d %b %Y")
            date_ms = date_object.timestamp() * 1000

            news = get_dictionary(headline, date_string, date_ms)

            arr_news.append(news)
        return arr_news

from datetime import datetime

from constants.NEWS import URL_NEWS_INFOSYS
from news.News import News, get_dictionary


class NewsInfosys(News):
    def __init__(self):
        self.url = URL_NEWS_INFOSYS
        super().__init__(self.url)

    def get_news(self):
        self.set_html()
        self.set_soup()

        cards = self.soup.find_all(class_="col-md-12 col-sm-12 col-xs-12 relative-off lng-txt")
        arr_news = []
        for card in cards:
            headline = card.find(class_="list-rslt-txt press-release-description").text.strip()
            date_string = card.find(class_="lct-txt press-release-date").text.strip()
            date_object = datetime.strptime(date_string, "%d %b %Y")
            date_ms = date_object.timestamp() * 1000

            news = get_dictionary(headline, date_string, date_ms)

            arr_news.append(news)
        return arr_news

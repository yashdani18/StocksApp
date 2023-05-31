from constants.NEWS import URL_NEWS_TATA_MOTORS
from news.News import News, get_dictionary
from datetime import datetime


class NewsTataMotors(News):
    def __init__(self):
        self.url = URL_NEWS_TATA_MOTORS
        super().__init__(self.url)

    def get_news(self):
        self.set_html()
        self.set_soup()
        list_news = self.soup.find(class_="pressrelease_list").find_all('li')
        arr_news = []
        for news in list_news:
            news_date = news.find(class_="date")
            headline = news.find('h3')
            news_body = news.find_all('p')
            # print("|" + str(type(headline)) + "|")
            if str(type(headline)) != "<class 'NoneType'>":
                date_in_ms = datetime.strptime(news_date.text, '%d %B, %Y').timestamp() * 1000

                dict_news = get_dictionary(headline.text, news_date.text, date_in_ms)

                arr_news.append(dict_news)
        # print(arr_news)
        return arr_news

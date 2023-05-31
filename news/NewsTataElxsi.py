from constants.NEWS import URL_NEWS_TATA_ELXSI
from news.News import News


class NewsTataElxsi(News):
    def __init__(self):
        self.url = URL_NEWS_TATA_ELXSI
        super().__init__(self.url)

    def get_news(self):
        self.set_html()
        self.set_soup()
        content = self.soup.find(id="content")

        headlines = content.find_all('h6')
        date = content.find_all('p')

        arr_news = []

        for index, headline in enumerate(headlines):
            dict_news = {
                'headline': headline.find('a').text,
                'date': date[index].text
            }
            arr_news.append(dict_news)
        return arr_news

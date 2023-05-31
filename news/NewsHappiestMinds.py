import news.News
from constants.NEWS import URL_NEWS_HAPPIEST_MINDS
from news.News import News, get_date_in_ms, get_dictionary


class NewsHappiestMinds(News):
    def __init__(self):
        self.url = URL_NEWS_HAPPIEST_MINDS
        super().__init__(self.url)

    def get_news(self):
        self.set_html()
        self.set_soup()

        tech_box = self.soup.find_all(class_='tech_box')

        arr_news = []

        for box in tech_box:
            headline = box.find('a').text.strip()
            date_string = box.find_all('p')[1].text.strip()
            split_string = date_string.split(',')
            concat_string = split_string[1].strip() + ' ' + split_string[2].strip()
            date_ms = get_date_in_ms(concat_string, "%B %d %Y")

            dict_news = get_dictionary(headline, date_string, date_ms)

            arr_news.append(dict_news)
        return arr_news

import news.News
from news.News import News, get_date_in_ms, get_dictionary
from constants.NEWS import DICTIONARY_HEADLINE, DICTIONARY_DATE_STRING, DICTIONARY_DATE_MS, URL_NEWS_TATA_POWER


class NewsTataPower(News):
    def __init__(self):
        self.url = URL_NEWS_TATA_POWER
        super().__init__(self.url)

    def get_news(self):
        self.set_html()
        self.set_soup()
        list_news = self.soup.find(class_="cont-search-results").find('ul').find_all('li')
        arr_news = []
        for news_item in list_news:
            headline = news_item.find('p').text
            date_string = news_item.find('b').text
            split_string = date_string.split(',')
            concat_string = split_string[1].strip() + ' ' + split_string[2].strip()
            date_ms = get_date_in_ms(concat_string, "%d %B %Y")

            dict_news = get_dictionary(headline, date_string, date_ms)

            arr_news.append(dict_news)
        # print(arr_news)
        return arr_news

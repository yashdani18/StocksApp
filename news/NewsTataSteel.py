import news.News
from news.News import News, get_date_in_ms
from constants.NEWS import URL_NEWS_TATA_STEEL


class NewsTataSteel(News):
    def __init__(self):
        self.url = URL_NEWS_TATA_STEEL
        super().__init__(self.url)

    def get_news(self):
        """Make request to get html, initialize soup and extract data fields"""
        self.set_html()
        self.set_soup()
        # use soup to extract data
        cards = self.soup.find_all(class_="card")
        arr_news = []
        for card in cards:
            # extract headline, date and calculate date in milliseconds
            headline = card.find('strong').text
            date_location_spans = card.find(class_="date-day").find_all('span')
            date_string = date_location_spans[0].text.strip() if len(date_location_spans) < 2 else date_location_spans[
                1].text.strip()
            date_ms = get_date_in_ms(date_string, "%B %d, %Y")

            dict_news = news.News.get_dictionary(headline, date_string, date_ms)

            arr_news.append(dict_news)
        # print(arr_news)
        return arr_news

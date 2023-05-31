from datetime import datetime

import requests
from bs4 import BeautifulSoup

DICTIONARY_HEADLINE = 'headline'
DICTIONARY_DATE_STRING = 'date_string'
DICTIONARY_DATE_MS = 'date_ms'


def get_date_in_ms(date_string, date_format):
    return datetime.strptime(date_string, date_format).timestamp() * 1000


def get_dictionary(headline, date_string, date_ms):
    return {
        DICTIONARY_HEADLINE: headline,
        DICTIONARY_DATE_STRING: date_string,
        DICTIONARY_DATE_MS: date_ms
    }


class News:
    def __init__(self, url):
        self.url = url
        self.html = ''
        self.soup = None
        self.DICTIONARY_HEADLINE = 'headline'
        self.DICTIONARY_DATE_STRING = 'date_string'
        self.DICTIONARY_DATE_MS = 'date_ms'

    def set_html(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/50.0.2661.102 Safari/537.36 '
        }
        self.html = requests.get(self.url, headers=headers).text
        return self.html

    def set_soup(self):
        self.soup = BeautifulSoup(self.html, 'lxml')

    def get_news(self):
        return []

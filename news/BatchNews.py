import time

from news.News import News
from news.NewsGodrejConsumerProducts import NewsGodrejConsumerProducts
from news.NewsHCLTech import NewsHCLTech
from news.NewsHappiestMinds import NewsHappiestMinds
from news.NewsInfosys import NewsInfosys
from news.NewsTVSMotors import NewsTVSMotors
from news.NewsTataConsultancyServices import NewsTataConsultancyServices
from news.NewsTataConsumer import NewsTataConsumer
from news.NewsTataMotors import NewsTataMotors
from news.NewsTataPower import NewsTataPower
from news.NewsTataSteel import NewsTataSteel


def fetch_news_from_company(news_object: News):
    return news_object.get_news()


objects = [NewsGodrejConsumerProducts(),
           NewsHappiestMinds(),
           NewsHCLTech(),
           NewsInfosys(),
           NewsTataConsultancyServices(),
           NewsTataConsumer(),
           NewsTataMotors(),
           NewsTataPower(),
           NewsTataSteel(),
           NewsTVSMotors()]


for obj in objects:
    dictionary = fetch_news_from_company(obj)
    print(dictionary[0:3])
    print()
    time.sleep(1)
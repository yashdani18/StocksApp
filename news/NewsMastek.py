from news.News import News


class NewsMastek(News):
    def __init__(self, url):
        super().__init__(url)

    def get_news(self):
        self.set_html()
        self.set_soup()
        yearItems = self.soup.find_all(True, {'class': ['accordion-item', 'invBox', 'mb-3']})
        print(len(yearItems))
        dictionary = []
        for yearItem in yearItems:
            year = yearItem.find(True, {'class': ['accordion-header', 'titleText']})
            if year is not None:
                # print(year.text)
                newsListings = yearItem.find(class_="newsListing")
                for newsListing in newsListings:
                    elements = newsListing.text.strip().split("\n")
                    if len(elements) >= 2:
                        headline = elements[0]
                        date = elements[1].split(year.text)[0] + year.text
                        # print(date)
                        news = {
                            'headline': headline,
                            'date': date
                        }
                        dictionary.append(news)
                        # print('headline', elements[0])
                        # print('date', elements[1].split(year.text)[0] + year.text)
                        # print()

        return dictionary

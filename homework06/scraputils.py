import requests
from bs4 import BeautifulSoup


def extract_news(soup):
    """ Extract news from a given web page """

    news_list = []
    try:
        table = soup.table.findAll('table')[1]
    except AttributeError:
        return

    for i in range(0, 89, 3):
        try:
            tr0 = table.findAll('tr')[i]
            tr1 = table.findAll('tr')[i + 1]

            td_for0 = tr0.findAll('td')[2]
            url = td_for0.a['href']
            # print(url)
            title = td_for0.a.text
            # print(title)

            td_for1 = tr1.findAll('td')[1]
            points = td_for1.find('span', {"class": "score"}).text
            if points:
                points = points.rsplit(' ', 1)[0]
            else:
                points = 0
            #  print(points)

            author_ = td_for1.find('a', {"class": "hnuser"}).text
            if author_:
                author = author_
            else:
                author = None
            # print(author)

            comments = "0"
            comment = td_for1.findAll('a')[-1].text
            if 'discuss' == comment:
                comments = 'discuss'
            else:
                comments = comment

            # print(comments)

            news = {'author': author,
                    'title': title,
                    'comments': comments,
                    'points': points,
                    'url': url}
            news_list.append(news)
        except AttributeError:

            pass
    # print(news_list)
    return news_list


def extract_next_page(soup):
    """ Extract next page URL """
    next = soup.find('a', {"class": "morelink"})
    return next['href']


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

import string

from bottle import (
    route, run, template, request, redirect
)
from sqlalchemy.orm import load_only

from bayes import NaiveBayesClassifier
from db import News, session
from scraputils import get_news

pages = 1


@route('/')
@route('/hello/<name>')
def greet(name='Stranger'):
    return template('Hello {{name}}, how are you?', name=name)


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    # 1. Получить значения параметров label и id из GET-запроса
    label = request.query.label
    news_id = request.query.id

    # 2. Получить запись из БД с соответствующим id (такая запись только одна!)
    news = s.query(News).filter(News.id == news_id).one()
    # 3. Изменить значение метки записи на значение label
    news.label = label
    # 4. Сохранить результат в БД
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    # 1. Получить данные с новостного сайта
    global pages
    newsdict = get_news('https://news.ycombinator.com/' + "news?p=" + str(pages), 1)
    pages = pages + 1
    # 2. Проверить, каких новостей еще нет в БД. Будем считать,
    #    что каждая новость может быть уникально идентифицирована
    #    по совокупности двух значений: заголовка и автора
    ex_news = s.query(News).options(load_only("title", "author")).all()
    ex_tit_au = [(news.title, news.author) for news in ex_news]
    for news in newsdict:
        if (news['title'], news['author']) not in ex_tit_au:
            news_add = News(title=news['title'],
                            author=news['author'],
                            url=news['url'],
                            comments=news['comments'],
                            points=news['points'])
            print(news_add)
            print('/n')
            s.add(news_add)
    # 3. Сохранить в БД те новости, которых там нет
    s.commit()
    print('end')
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    labeled_news = s.query(News).filter(News.label != None).all()
    x_train = [clean(news.title) for news in labeled_news]
    y_train = [news.label for news in labeled_news]
    classifier.fit(x_train, y_train)

    rows = s.query(News).filter(News.label == None).all()
    good, maybe, never = [], [], []
    for row in rows:
        prediction = classifier.predict(clean(row.title))
        if prediction == 'good':
            good.append(row)
        elif prediction == 'maybe':
            maybe.append(row)
        else:
            never.append(row)

    return template('classified', good=good, maybe=maybe, never=never)


def clean(s):
    translator = str.maketrans('', '', string.punctuation)  # удаление знаков препинания
    return s.translate(translator).lower()


if __name__ == "__main__":
    classifier = NaiveBayesClassifier()
    run(host="localhost", port=8080, debug=True)

import datetime
from collections import Counter
from typing import List, Tuple
import plotly
import plotly.graph_objs as go
import plotly.plotly as py
import config
from api_models import Message

Dates = List[datetime.date]
Frequencies = List[int]

plotly.tools.set_credentials_file(
    username=config.PLOTLY_CONFIG['username'],
    api_key=config.PLOTLY_CONFIG['api_key']
)


def fromtimestamp(ts: int) -> datetime.date:
    return datetime.datetime.fromtimestamp(ts).date()


def count_dates_from_messages(messages: List[Message]) -> Tuple[Dates, Frequencies]:
    """ Получить список  дат и их частот

    :param messages: список сообщений
    """
    # считается количество повторяющихся дат сообщений
    c = Counter()
    for message in messages:
        date = fromtimestamp(message.date)
        c[date] += 1
    # * превращает итератор в отдельные аргументы
    # zip() на каждой итерации возвращает кортэж, содержащий элементы
    # ...возвращает объект, поддерживающий итерации
    result = list(zip(*c.most_common()))
    if len(result) == 0:
        return ([], [])
    return tuple((sorted(result[0]), [c[date] for date in sorted(result[0])]))


def plotly_messages_freq(dates: Dates, freq: Frequencies) -> None:
    """ Построение графика с помощью Plot.ly

    :param date: список дат
    :param freq: число сообщений в соответствующую дату
    """

    x = dates

    data = [go.Scatter(x=x, y=freq)]
    py.iplot(data)

    return None

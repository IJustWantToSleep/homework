import datetime
from datetime import date
from statistics import median
from typing import Optional

from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди  возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    curdate = datetime.date.today()
    friends = [User(**i) for i in get_friends(user_id, 'bdate')]
    # bdates = get_friends(user_id, 'bdate')
    bdates = []
    # в блоке try выполн. инструкция, except - исключение
    for friend in friends:
        birthday = friend.bdate
        try:
            age = calculate_age(datetime.datetime.strptime(birthday, "%d.%m.%Y"))
            bdates.append(age)
        except (ValueError, TypeError):
            pass

    if bdates:
        return float(median(bdates))


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

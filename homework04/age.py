import datetime as dt
from statistics import median
from typing import Optional

from api import get_friends
from api_models import User
import time
import datetime


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

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
            # time.strptime преобразует строку в datetime
            bdates = time.strptime(birthday, "%d.%m.%Y")
            # bdates = datetime.strptime(birthday, "%d.%m.%Y")
        except (ValueError, TypeError):
            pass
        else:
            age = curdate.year - bdates.year - ((curdate.month, curdate.day) < (bdates.month, bdates.day))
            bdates.append(age)
    if bdates:
        return float(median(bdates))


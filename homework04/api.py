import time

import requests

from config import VK_CONFIG as vk


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for x in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            return response
        except requests.exceptions.RequestException:
            if x == max_retries - 1:
                raise
            delay = backoff_factor * 2 ** x
            # time.sleep прерывает выполнение скрипта на заданное время
            # delay рассчитан с помощью коэффициента экспоненциального нарастания задержки
            time.sleep(delay)


def get_friends(user_id, fields):
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    query_params = {

        'access_token': vk['access_token'],
        'user_id': user_id,
        'fields': fields,
        'version': vk['version']
    }
    # содержимое format() вставляется в {}
    query = "{domain}/friends.get?".format(domain=vk['domain'])
    response = requests.get(query, query_params)
    json_doc = response.json()
    fail = json_doc.get('error')
    if fail:
        raise Exception(json_doc['error']['error_msg'])
    # return json_doc['response']['items']
    return response.json()


def messages_get_history(user_id, offset=0, count=200):
    """ Получить историю переписки с указанным пользователем

    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"

    query_params = {
        'domain': vk['domain'],
        'access_token': vk['access_token'],
        'user_id': user_id,
        'offset': offset,
        'count': count,
        'version': vk['version']
    }
    messages = []
    i = 0
    while i < count:
        # ограничение на число запросов в секунду - 3 запроса в секунду
        # за 1 запрос можно получить 200 сообщений
        # если больше нельзя делать запросы, исп. time.sleep
        # time.sleep прерывает выполнение скрипта на заданное время
        if (i / 200) % 3 == 0 and i:
            time.sleep(1)
        if count - i <= 200:
            query_params['count'] = count - i
        url = "{domain}/messages.getHistory?offset={offset}&count={count}&user_id={user_id}&" \
              "access_token={access_token}&v={version}".format(**query_params)
        response = requests.get(url)
        json_doc = response.json()
        fail = json_doc.get('error')
        if fail:
            raise Exception(json_doc['error']['error_msg'])
        messages.extend(json_doc['response']['items'])
        i += 200
        query_params['offset'] += i
    return messages

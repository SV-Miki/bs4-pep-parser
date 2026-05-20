"""Вспомогательные функции парсера."""

from requests import RequestException

from constants import DEFAULT_ENCODING
from exceptions import ParserFindTagException


def get_response(session, url, encoding=DEFAULT_ENCODING):
    """Загружает страницу и возвращает ответ сервера."""
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException as error:
        raise ConnectionError(
            f'Возникла ошибка при загрузке страницы {url}'
        ) from error


def find_tag(soup, tag, attrs=None, string=None):
    """Находит тег или вызывает исключение."""
    searched_tag = soup.find(tag, attrs=(attrs or {}), string=string)

    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        raise ParserFindTagException(error_msg)

    return searched_tag

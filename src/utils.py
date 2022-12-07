import logging

from requests import RequestException

from exceptions import ParserFindTagException, EmptyResponseException


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = "utf-8"
    except RequestException as ex:
        logging.exception(
            f"Возникла ошибка при загрузке страницы {url}", stack_info=True
        )
        raise ex

    if response is None:
        error_msg = "Response is None"
        logging.error(error_msg, stack_info=True)
        raise EmptyResponseException(error_msg)

    return response


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f"Не найден тег {tag} {attrs}"
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag

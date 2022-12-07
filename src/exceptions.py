class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""

    pass


class EmptyResponseException(Exception):
    """Вызывается, когда response is None"""

    pass

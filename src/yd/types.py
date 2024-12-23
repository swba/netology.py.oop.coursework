from typing import TypedDict, Literal


class YDError(Exception):
    """Custom exception for YandexDisk API errors."""
    pass


class YDResponse(TypedDict):
    """
    Format of Yandex Disk API responses which seems to be common for
    all endpoints.

    """
    href: str
    method: Literal['GET', 'PUT']
    templated: Literal['true', 'false']
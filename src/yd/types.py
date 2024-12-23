from typing import TypedDict, Literal


class YDError(Exception):
    """Custom exception for Yandex Disk API errors."""
    pass


class YDResponse(TypedDict):
    """General Yandex Disk API response's format.

    """
    href: str
    method: Literal['GET', 'PUT']
    templated: Literal['true', 'false']

from typing import Literal, Required, TypedDict


class VKError(Exception):
    """Custom exception for VK API errors."""
    pass


class VKGeneralParams(TypedDict, total=False):
    """
    General API parameters.
    @see https://dev.vk.com/en/api/api-requests#General%20parameters

    """
    lang: Literal['ru', 'uk', 'be', 'en', 'es', 'fi', 'de', 'it']
    test_mode: Literal[0, 1]


class VKPhotosGetParams(VKGeneralParams, total=False):
    """
    Parameters of the photos.get endpoint.
    Note that this type doesn't include `owner_id` and `album_id`
    parameters, which are required
    @see https://dev.vk.com/en/method/photos.get#Parameters

    """
    owner_id: Required[str]
    album_id: str
    photo_ids: str
    rev: Literal[0, 1]
    extended: Literal[0, 1]
    feed_type: str
    feed: int
    photo_sizes: Literal[0, 1]
    offset: int
    count: int

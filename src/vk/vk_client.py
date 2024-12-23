import requests

from .types import VKError, VKPhotosGetParams


class VKClient:
    """
    VK API client.
    @see https://dev.vk.com/ru/reference

    """

    BASE_URL = 'https://api.vk.com/method/'

    def __init__(self, token: str, version: str = '5.199'):
        self.__token = token
        self.__version = version

    def _request(self, path: str, params: dict = None):
        """Sends arbitrary requests to the API."""
        url = VKClient.BASE_URL + path.lstrip('/')
        params = {
            **(params or {}),
            'access_token': self.__token,
            'v': self.__version
        }
        response = requests.post(url, params=params)
        match response.status_code:
            case 200:
                json = response.json()
                if 'error' in json:
                    error = json['error']
                    raise VKError(f'(Error code: {error["error_code"]}) {error["error_msg"]}')
                elif 'response' in json:
                    return json['response']
                else:
                    raise VKError('Unknown server error')
            case _:
                raise VKError(f'Server error ({response.status_code})')

    def photos_get(self, params: VKPhotosGetParams):
        """
        Returns photos from an album.
        @see https://dev.vk.com/ru/method/photos.get

        """
        params = {
            # Add sane default parameters.
            'extended': 1,
            'album_id': 'profile',
            **(params or {}),
        }
        return self._request('photos.get', params=params)

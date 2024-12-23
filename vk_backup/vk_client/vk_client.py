import requests

from .vk_types import VKError, VKPhotosGetParams


class VKClient:
    """VK API client.
    See https://dev.vk.com/ru/reference

    """

    BASE_URL = 'https://api.vk.com/method/'

    def __init__(self, token: str, version: str = '5.199'):
        """Creates a VK API client.

        Args:
            token: Access token for VK API.
            version: VK API version. Defaults to "5.199".

        """
        self.__token = token
        self.__version = version

    def _request(self, path: str, params: dict = None) -> dict:
        """Sends arbitrary requests to VK API.

        Args:
            path: Endpoint path like "photos.get".
            params: Endpoint parameters, if any. Defaults to None.

        Returns:
            Parsed endpoint's response.

        Raises:
            VKError: If VK API responded with an error.

        """
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

    def photos_get(self, params: VKPhotosGetParams) -> dict:
        """Returns photos from a VK album.
        See https://dev.vk.com/ru/method/photos.get

        Args:
            params: Request parameters. ``owner_id`` is required, and
                default value for ``album_id`` is "profile".

        Returns:
            Parsed endpoint response containing photos information.

        Raises:
            VKError: If VK API responded with an error.

        """
        params = {
            # Set default album_id value.
            'album_id': 'profile',
            **(params or {}),
        }
        return self._request('photos.get', params=params)

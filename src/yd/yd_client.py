import requests
from typing import AnyStr

from .types import YDError, YDResponse


class YDClient:
    """YandexDisk API client.
    @see https://yandex.ru/dev/disk-api/doc/ru/

    """

    BASE_URL = 'https://cloud-api.yandex.net/v1/disk/'

    def __init__(self, token: str):
        """Creates a Yandex Disk API client.

        Args:
            token: Access token for Yandex Disk API.

        """
        self.__token = token

    def _request(self, method: str, name: str = '', params: dict = None) -> YDResponse:
        """Sends arbitrary requests to the API.

        Args:
            method: Request method like "GET" or "PUT".
            name: Endpoint name like "resources/upload.
            params: Endpoint parameters.

        Returns:
            Parsed response from Yandex Disk API.

        Raises:
            YDError: If Yandex Disk API responded with an error.

        """
        url = YDClient.BASE_URL + name.lstrip('/')
        headers = {
            'Authorization': f'OAuth {self.__token}'
        }
        response = requests.request(method, url, headers=headers, params=params)
        json = response.json()
        match response.status_code // 100:
            case 2:
                return json
            case _:
                raise YDError(f'({json["error"]}) {json["description"]}')

    def capacity(self):
        """Requests general information about the user's Yandex Disk.
        @see https://yandex.ru/dev/disk-api/doc/en/reference/capacity

        Returns:
            Parsed response from Yandex Disk API.

        Raises:
            YDError: If Yandex Disk API responded with an error.

        """
        return self._request('GET')

    def folder_create(self, path: str) -> YDResponse:
        """Creates a folder on Yandex Disk.

        Args:
            path: Path to a folder to create.

        Returns:
            Parsed response from Yandex Disk API.

        Raises:
            YDError: If Yandex Disk API responded with an error.

        """
        return self._request('PUT', 'resources', {'path': path})

    def file_upload(self, file: AnyStr, path: str, overwrite: bool = False) -> True:
        """Uploads a file to Yandex Disk.
        @see https://yandex.ru/dev/disk-api/doc/ru/reference/upload

        Args:
            file: File to upload.
            path: Path to a file on Yandex Disk including folders and filename.
            overwrite: Whether to overwrite existing file. Defaults to False.

        Returns:
            True, if everything went OK. Otherwise, an exception is raised.

        Raises:
            YDError: If Yandex Disk API responded with an error.

        """
        # Get upload URL.
        params = {'path': path, 'overwrite': overwrite}
        res = self._request('GET', 'resources/upload', params)
        # Do upload the file.
        href, method = res['href'], res['method']
        res = requests.request(method, href, files={'file': file})
        match res.status_code:
            case 412:
                raise YDError('412 Precondition Failed')
            case 413:
                raise YDError('413 Payload Too Large')
            case 500:
                raise YDError('500 Internal Server Error')
            case 503:
                raise YDError('503 Service Unavailable')
            case 507:
                raise YDError('507 Insufficient Storage')
        return True
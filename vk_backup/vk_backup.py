from datetime import date
import json
import requests

from .vk_client import VKClient
from .vk_types import VKPhotosGetParams
from .yd_client import YDClient
from .yd_types import YDError


class VKBackup:
    """Backs up photos from VK to cloud drive."""

    def __init__(self, token: str, disk_params: dict):
        """Creates a new class instance.

        Args:
            token: Access token for VK API.
            disk_params: Parameters to get access to a disk API used to
                save the photos.

        """
        self._vk = VKClient(token)
        match disk_params['type'].lower():
            case 'yd':
                self._yd = YDClient(disk_params['token'])

    def backup(self, photos_params: VKPhotosGetParams, folder: str = None,
                     overwrite: bool = False):
        """Saves photos from VK to a cloud disk.

        Args:
            photos_params: Parameters/filter to get photos from VK API.
                See https://dev.vk.com/ru/method/photos.get.
                The only required parameter is ``owner_id``; ``album_id``
                is equal to "profile" by default. Also, note that
                ``extended`` is always 1, as likes info is required to
                prepare names of photos being uploaded.
            folder: Folder to save photos to. If is equal to None (by
                default), all the photos will be saved to a folder
                named "VK Photos (Y-m-d)" (for current date).
            overwrite: Whether to overwrite existing photos. Defaults to
                False.

        Raises:
            VKError: If VK API responded with an error.
            YDError: If Yandex Disk API responded with an error.

        """
        print('Fetching photos information...')

        # Get the list of photos.
        res = self._vk.photos_get(photos_params | {'extended': 1})
        photos = res['items']

        # Prepare a folder to upload photos to.
        if folder is None:
            folder = f'VK Photos ({date.today().isoformat()})'

        # Do backup photos.
        if self._yd:
            self._save_to_yandex_disk(photos, folder, overwrite)

    def _save_to_yandex_disk(self, photos: list, folder: str, overwrite: bool = False):
        """Saves photos to Yandex Disk.

        Args:
            photos: List of photos.
                See https://dev.vk.com/en/reference/objects/photo.
            folder: Folder to save photos to.
            overwrite: Whether to overwrite existing photos. Defaults to False.

        Raises:
            YDError: If Yandex Disk API responded with an error.

        """
        print(f'Saving {len(photos)} photos to Yandex Disk, folder {folder}.')

        # Create a folder if it doesn't exist yet.
        try:
            print(f'Creating folder {folder}... ', end='')
            self._yd.folder_create(folder)
            print('Success!')
        except YDError as e:
            # Do not raise the exception if the folder already exists,
            # as the user is probably aware of this and doesn't care.
            print(e)

        # Info which is going to be saved into a file afterward.
        photos_info = []

        # Set of already used filenames to not repeat them.
        filenames = set()

        # Download photos from VK and then upload to Yandex Disk,
        # one by one.
        for i, photo in enumerate(photos):
            print(f'Processing photo {i + 1} of {len(photos)}: ', end='')
            # Original photo is always the largest among all sizes.
            url = photo['orig_photo']['url']
            res = requests.get(url)
            if res.status_code == 200:
                print('Downloaded... ', end='')
                # Prepare the filename.
                # Do all VK photos have JPG format, or should we parse
                # photo URL to get its extension?
                filename = f'{photo["likes"]["count"]}.jpg'
                if filename in filenames:
                    filename = f'{photo["likes"]["count"]}-{photo["date"]}.jpg'
                filenames.add(filename)
                # Upload file to Yandex Disk and log the result.
                try:
                    self._yd.file_upload(res.content, f'{folder}/{filename}', overwrite)
                    photos_info.append({
                        'file_name': filename,
                        'size': 'base',
                    })
                    print('Saved to Yandex Disk!')
                except YDError as e:
                    print(e)
            else:
                print(f'Error downloading ({res.status_code})')

        # Save photos info into a file.
        filename = 'backup.json'
        print(f'Saving report ({filename}) to the working directory: ', end='')
        with open(filename, 'w', encoding='UTF-8') as f:
            json.dump(photos_info, f, ensure_ascii=False, indent=4)
            print('Success!')

        # Also save it to Yandex Disk to the same folder where
        # photos were saved. Just in case.
        print(f'Saving report ({filename}) to Yandex Disk: ', end='')
        file = json.dumps(photos_info,  ensure_ascii=False, indent=4)
        try:
            self._yd.file_upload(file, f'{folder}/{filename}', True)
            print('Success!')
        except YDError as e:
            print(e)

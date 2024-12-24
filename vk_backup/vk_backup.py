from datetime import date
import json
import os
import time
import requests

from .vk_client import VKClient, VKPhotosGetParams
from .yd_client import YDClient, YDError
from .logger import Logger


class VKBackup:
    """Backs up photos from VK to cloud drive."""

    def __init__(self, vk_token: str, yd_token: str):
        """Creates a new class instance.

        Args:
            vk_token: Access token for VK API.
            yd_token: Access token for Yandex Disk API.

        """
        self._vk = VKClient(vk_token)
        self._yd = YDClient(yd_token)

    def backup(self, photos_params: VKPhotosGetParams, folder: str = None,
                     overwrite: bool = False, json_folder: str = None):
        """Saves photos from VK to a cloud disk.

        Args:
            photos_params: Parameters/filter to get photos from VK API.
                See https://dev.vk.com/ru/method/photos.get.
                The only required parameter is ``owner_id``; ``album_id``
                is equal to "profile" and ``count`` is equal to 5 by
                default. Also, note that ``extended`` is always 1, as
                likes info is required to prepare names of photos being
                uploaded.
            folder: Folder on Yandex Disk to save photos to. If is equal
                to None (by default), all the photos will be saved to a
                folder named "VK Photos (Y-m-d)" (for current date).
            overwrite: Whether to overwrite existing photos. Defaults to
                False.
            json_folder: Local folder to save information about backed
                up files to. If is equal to None (by default), a
                relative folder ``output`` is used.

        Raises:
            VKError: If VK API responded with an error.
            YDError: If Yandex Disk API responded with an error.

        """
        Logger.info('Fetching photos information...')

        # Get the list of photos.
        res = self._vk.photos_get(photos_params | {'extended': 1})
        photos = res['items']

        # Prepare a folder to upload photos to.
        if folder is None:
            folder = f'VK Photos ({date.today().isoformat()})'

        Logger.info(f'Saving {len(photos)} photos to Yandex Disk, folder "{folder}".')

        # Create a folder if it doesn't exist yet.
        try:
            Logger.info(f'Creating folder "{folder}"... ', end='')
            self._yd.folder_create(folder)
            Logger.success('Success!')
        except YDError as e:
            # Do not raise the exception if the folder already exists,
            # as the user is probably aware of this and doesn't care.
            Logger.warning(e)

        # Backup info which is going to be saved into a file afterward.
        backup_info = []

        # Set of already used filenames to not repeat them.
        filenames = set()

        # Download photos from VK and then upload to Yandex Disk,
        # one by one.
        for i, photo in enumerate(photos):
            Logger.info(f'Processing photo {i + 1} of {len(photos)}: ', end='')
            # Original photo is always the largest among all sizes.
            url = photo['orig_photo']['url']
            res = requests.get(url)
            if res.status_code == 200:
                Logger.success('Downloaded... ', end='')
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
                    backup_info.append({
                        'file_name': filename,
                        'size': 'base',
                    })
                    Logger.success('Saved to Yandex Disk!')
                except YDError as e:
                    Logger.warning(e)
            else:
                Logger.error(f'Error downloading ({res.status_code})')

        # Prepare name of a file to save backup info to.
        filename = f'backup {int(time.time())}.json'

        # Save backup info into a local file.
        if json_folder is None:
            json_folder = 'output'
        Logger.info(f'Saving report ({filename}) to "{json_folder}" folder: ', end='')
        with open(os.path.join(os.getcwd(), json_folder, filename), 'w', encoding='UTF-8') as f:
            json.dump(backup_info, f, ensure_ascii=False, indent=4)
            Logger.success('Success!')

        # Also save it to Yandex Disk to the same folder where
        # photos were saved. Just in case.
        Logger.info(f'Saving report ({filename}) to Yandex Disk: ', end='')
        file = json.dumps(backup_info,  ensure_ascii=False, indent=4)
        try:
            self._yd.file_upload(file, f'{folder}/{filename}', True)
            Logger.success('Success!')
        except YDError as e:
            Logger.error(e)

        Logger.info('Thanks everyone!\n')

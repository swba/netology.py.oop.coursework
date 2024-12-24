import json
from time import time
import os
from pytest import raises

from vk_backup.yd_client import YDClient, YDError


class TestYd:

    @staticmethod
    def get_token() -> str:
        """Returns Yandex Disk API token."""
        with open(os.path.join(os.getcwd(), os.pardir, 'tokens.json')) as f:
            tokens = json.load(f)
        return tokens['yd']

    def test_connection(self):
        """Tests connection to Yandex Disk."""
        token = self.get_token()

        # Test request with incorrect token.
        with raises(YDError) as e:
            yd = YDClient(token + '!')
            yd.capacity()
            assert e.value == '(UnauthorizedError) Unauthorized'

        # Test correct token.
        yd = YDClient(token)
        assert type(yd.capacity()) == dict

    def test_folder_create(self):
        """Tests YDClient.folder_create() method."""
        token = self.get_token()
        yd = YDClient(token)

        folder = f'test-create-{time()}'

        # Test creating a top-level folder.
        res = yd.folder_create(folder)
        assert res['href'] == f'https://cloud-api.yandex.net/v1/disk/resources?path=disk%3A%2F{folder}'

        # Test creating existing folder.
        with raises(YDError) as e:
            yd.folder_create(folder)
            assert str(e.value).startswith('(DiskPathPointsToExistentDirectoryError)')

        # Test creating a nested folder.
        res = yd.folder_create(f'{folder}/nested')
        assert res['href'] == f'https://cloud-api.yandex.net/v1/disk/resources?path=disk%3A%2F{folder}%2Fnested'

    def test_file_upload(self):
        """Tests YD.file_upload() method."""
        token = self.get_token()
        yd = YDClient(token)

        folder = f'test-upload-{time()}'
        yd.folder_create(folder)

        with open(os.path.join(os.getcwd(), 'data', 'test_upload.jpg'), 'rb') as upload_file:
            path = f'{folder}/test_upload.jpg'
            upload = upload_file.read()

            # Test uploading to a non-existing folder.
            assert yd.file_upload(upload, path) is True

            # Test uploading to an existing folder without overwrite.
            with raises(YDError) as e:
                yd.file_upload(upload, path, False)
                assert str(e.value).startswith('(DiskResourceAlreadyExistsError)')

            # Test uploading to an existing folder with overwrite.
            assert yd.file_upload(upload, path, True) is True

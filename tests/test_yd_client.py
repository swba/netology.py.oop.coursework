from time import time
from pytest import raises

from vk_backup import YDClient, YDError


class TestYd:

    def test_connection(self):
        """Tests connection to Yandex Disk."""
        with open('tokens/.yd') as f:
            token = f.read()

            # Test request with incorrect token.
            with raises(YDError) as e:
                yd = YDClient(token + '!')
                yd.capacity()
                assert e.value == '(UnauthorizedError) Unauthorized'

            yd = YDClient(token)
            assert type(yd.capacity()) == dict

    def test_folder_create(self):
        """Tests YDClient.folder_create() method."""
        with open('tokens/.yd') as f:
            token = f.read()
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
        with open('tokens/.yd') as token_file:
            token = token_file.read()
            yd = YDClient(token)

            folder = f'test-upload-{time()}'
            yd.folder_create(folder)

            with open('assets/upload.jpg', 'rb') as upload_file:
                path = f'{folder}/upload.jpg'
                upload = upload_file.read()

                # Test uploading to a non-existing folder.
                assert yd.file_upload(upload, path) is True

                # Test uploading to an existing folder without overwrite.
                with raises(YDError) as e:
                    yd.file_upload(upload, path, False)
                    assert str(e.value).startswith('(DiskResourceAlreadyExistsError)')

                # Test uploading to an existing folder with overwrite.
                assert yd.file_upload(upload, path, True) is True

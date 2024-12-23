import json
import os
from pytest import raises

from vk_backup.vk_client import VKClient, VKError


class TestVK:

    VK_USER_ID = '153151548'

    @staticmethod
    def get_token() -> str:
        """Returns VK API token."""
        with open(os.path.join(os.getcwd(), os.pardir, 'tokens.json')) as f:
            tokens = json.load(f)
        return tokens['vk']

    def test_photos_get(self):
        """Tests. VKClient.photos_get() method."""
        token = self.get_token()

        # Test access denied error with incorrect token.
        with raises(VKError) as e:
            vk = VKClient(token + '!')
            vk.photos_get({'owner_id': self.VK_USER_ID})
            assert e.value == '(Error code: 5) User authorization failed: invalid access_token (4)'

        vk = VKClient(token)

        # Test incorrect user ID format.
        with raises(VKError) as e:
            vk.photos_get({'owner_id': self.VK_USER_ID + '!'})
            assert e.value == '(Error code: 100) One of the parameters specified was missing or invalid: owner_id not integer'

        # Test incorrect (missing) user ID.
        with raises(VKError) as e:
            vk.photos_get({'owner_id': self.VK_USER_ID + '99999999'})
            assert e.value == '(Error code: 113) Invalid user id'

        # Test correct request with default parameters.
        photos = vk.photos_get({'owner_id': self.VK_USER_ID})
        assert photos['items'][0]['id'] == 456239017

        # Test fetching photos from the wall.
        photos = vk.photos_get({
            'owner_id': self.VK_USER_ID,
            'album_id': 'wall'
        })
        assert photos['count'] == 7

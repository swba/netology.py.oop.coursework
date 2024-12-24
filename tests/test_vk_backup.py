from vk_backup import VKBackup

class TestVKBackup:

    VK_USER_ID = '153151548'

    def test_backup_yd(self):
        """Tests VKBackup.backup() method for Yandex Disk."""
        with open('.tokens/.vk') as token_vk_file:
            with open('.tokens/.yd') as token_yd_file:
                token_vk = token_vk_file.read()
                token_yd = token_yd_file.read()

                backup = VKBackup(token_vk, {
                    'type': 'yd',
                    'token': token_yd,
                })

                backup.backup({'owner_id': self.VK_USER_ID})

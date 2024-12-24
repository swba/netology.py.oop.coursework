import json
from vk_backup import VKBackup

if __name__ == '__main__':

    VK_USER_ID = '153151548'

    # Get API tokens.
    with open('tokens.json') as f:
        tokens = json.load(f)

    # Create a backuper instance.
    backup_yd = VKBackup(tokens['vk'], tokens['yd'])

    # Save photos from profile to a default folder.
    backup_yd.backup({'owner_id': VK_USER_ID})

    # Repeat and get errors that everything already exists.
    backup_yd.backup({'owner_id': VK_USER_ID})

    # Repeat and overwrite everything.
    backup_yd.backup({'owner_id': VK_USER_ID}, overwrite=True)

    # Save 6 photos from the wall to a specific folder.
    backup_yd.backup({'owner_id': VK_USER_ID, 'album_id': 'wall', 'count': 6}, folder="VK Wall!")

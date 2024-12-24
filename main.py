if __name__ == '__main__':
    from vk_backup import VKBackup

    VK_USER_ID = '153151548'
    TOKEN_VK = 'YOUR_VK_TOKEN'
    TOKEN_YD = 'YOUR_YANDEX_DISK_TOKEN'

    backup_yd = VKBackup(TOKEN_VK, {
        'type': 'yd',
        'token': TOKEN_YD,
    })

    # Save photos from profile to a default folder.
    backup_yd.backup({'owner_id': VK_USER_ID})

    # Repeat and get errors that everything already exists.
    backup_yd.backup({'owner_id': VK_USER_ID})

    # Repeat and overwrite everything.
    backup_yd.backup({'owner_id': VK_USER_ID}, overwrite=True)

    # Save 5 photos from the wall to a specific folder.
    backup_yd.backup({'owner_id': VK_USER_ID, 'album_id': 'wall'}, folder="VK Wall!")

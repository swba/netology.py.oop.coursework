if __name__ == '__main__':
    from vk_backup import VKBackup

    VK_USER_ID = '153151548'
    TOKEN_VK = 'YOUR_VK_TOKEN'
    TOKEN_YD = 'YOUR_YANDEX_DISK_TOKEN'

    backup_yd = VKBackup(TOKEN_VK, {
        'type': 'yd',
        'token': TOKEN_YD,
    })
    backup_yd.backup({'owner_id': VK_USER_ID, 'album_id': 'wall'})

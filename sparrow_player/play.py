"""module play"""
import os

import logging_adaptor as logging
import media_list
import nfs
import hot_key
from player import player
from configparser import ConfigParser


LOG = logging.get_logger(__name__)

# @ -------- GLOBAL --------
# MEDIA_PLAYER = None
JUMP = False
NFS_LOCAL_PATH = "/home/pi/Desktop/nfs"
CONFIG_FILE = "/etc/sparrow-player/config.ini"


def hotkey_jump():
    """hot key"""
    LOG.debug('media play break from hotkey')
    global JUMP
    JUMP = True
    player.stop()


def test_for_database():
    """test for database"""
    LOG.debug('in test')
    # Test
    import random

    r = random.randint(1, 10000)
    media_name = 'name' + str(r)
    media_path = 'path' + str(r)

    m = media_list.MediaList()
    m.add(path=media_path, name=media_name)

    vid = m.get_id_by_path(media_path)
    m.increase_fail_count(vid)
    m.increase_play_count(vid)
    m.increase_jump_count(vid)
    # m.update_priority(vid)
    m.update_priority(vid, action='low')
    m.update_name(vid, 'a new name')

    list_all = m.get_list_all()
    for one in list_all:
        # LOG.debug('-' * 20)
        m.show_info(one)
        # LOG.debug(one.name)
        m.delete_by_id(one.id)


def play():
    """play"""
    all_medias = media_list.MediaList(CONFIG_FILE)

    while True:
        one = all_medias.get_random()
        content = NFS_LOCAL_PATH + one
        name = all_medias.get_name_by_path(one)

        if os.path.isfile(content):
            LOG.debug("going to play media: %s", content)
            player.play(content, name)

        elif os.path.isdir(content):
            LOG.debug("going to directory media: %s", content)
            files = os.listdir(content)
            files.sort()

            for file_name in files:
                abs_path = content + "/" + file_name
                player.play(abs_path, name)

                global JUMP
                if JUMP:
                    JUMP = False
                    break
        else:
            LOG.warning("`%s` is not a file nor a directory.", content)


def main():
    """main"""
    try:
        LOG.debug('main start with config_file %s nfs_local_path %s', CONFIG_FILE, NFS_LOCAL_PATH)

        # 1. get nfs list
        nfs_instance = nfs.Nfs(NFS_LOCAL_PATH, CONFIG_FILE)
        nfs_instance.mount()
        contents = nfs_instance.get_list()
        # LOG.debug(contents)

        # 2. update database
        cfg = ConfigParser()
        cfg.read(CONFIG_FILE)

        db_config = cfg.__getitem__('database')

        server_ip = db_config.get('ip')
        username = db_config.get('username')
        db_name = db_config.get('db_name')
        # password = cs.get('password')

        all_medias = media_list.MediaList(server_ip, username, db_name)
        all_medias.find_new_to_add(contents)

        # 3. bind hotkey
        hot_key.HotKey().bind('q', hotkey_jump)

        # 5. Play
        play()

    except:
        LOG.exception("Somethin error")


if __name__ == '__main__':
    main()

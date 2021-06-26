"""module play"""
import os

import sys
from os.path import abspath, dirname
sys.path.append(dirname(dirname(abspath(__file__))))

import logging_adaptor as logging
import media_list
import nfs
import hot_key
from player import player
from sqlalchemy import exc


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


def play():
    """play"""
    medias = media_list.MediaList()

    while True:
        try:
            media_path = medias.get_random_media_path()
            media_full_path = NFS_LOCAL_PATH + media_path
            media_id = medias.get_id_by_path(media_path)
            media_title = medias.get_media_title_by_path(media_path)

            if os.path.isfile(media_full_path):
                LOG.debug("going to play media: %s", media_full_path)
                medias.increase_played(media_id)
                player.play(media_full_path, media_title)

            elif os.path.isdir(media_full_path):
                LOG.debug("going to directory media: %s", media_full_path)
                medias.increase_played(media_id)
                files = os.listdir(media_full_path)
                files.sort()

                for file_name in files:
                    abs_path = media_full_path + "/" + file_name
                    player.play(abs_path, media_title)

                    global JUMP
                    if JUMP:
                        JUMP = False
                        break
            else:
                LOG.warning("`%s` is not a file nor a directory.", media_full_path)
                continue

        except exc.NoResultFound as e:
            LOG.error('no result found %s', e)
            continue

        except exc.MultipleResultsFound as e:
            LOG.error('multiple results found: ', e)
            continue


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
        all_medias = media_list.MediaList()
        all_medias.find_new_to_add(contents)

        # 3. bind hotkey
        hot_key.HotKey().bind('q', hotkey_jump)

        # 5. Play
        play()

    except:
        LOG.exception("Somethin error")


if __name__ == '__main__':
    main()

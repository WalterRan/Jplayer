import logging_adaptor as logging
import os
import media_list
import nfs
from player import player
from flask import Flask
from threading import Thread
from HotKey import hotkey


# @ -------- LOGGING --------
LOG = logging.getLogger(__name__)

# @ -------- GLOBAL --------
media_player = None
jump = False
nfs_local_path = "/home/pi/Desktop/nfs"
config_file = "./config.ini"

# @ -------- CONFIG --------
# run_mode = 'local'
run_mode = 'remote'
directory = "/home/"
debug_mode = False
nfs_ip = "192.168.0.102"
nfs_dir = "/media/slot3_4t/media"
local_dir = "/home/pi/Desktop/nfs"

# @ -------- CONFIG end --------


# @ -------- RESTAPI --------
app = Flask(__name__)


@app.route('/')
def hello_world():
    return "hello world"


@app.route('/title/', methods=['GET'])
def rest_get_title():
    return str(player.get_title())


# curl --request POST 127.0.0.1:5000/next/
@app.route('/next/', methods=['POST'])
def rest_post_next():
    return str(player.stop())


def web_server():
    app.run()


def hotkey_jump():
    LOG.debug('media play break from hotkey')
    global jump
    jump = True
    player.stop()


def test_for_database():
    LOG.debug('in test')
    # Test
    import random

    r = random.randint(1, 10000)
    media_name = 'name' + str(r)
    media_path = 'path' + str(r)

    m = media_list.MediaList()
    m.create(path=media_path, name=media_name)

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
    m = media_list.MediaList(config_file)

    while True:
        one = m.get_random()
        content = nfs_local_path + one
        name = m.get_name_by_path(one)

        if os.path.isfile(content):
            LOG.debug("going to play media: %s", content)
            player.play(content, name)

        elif os.path.isdir(content):
            LOG.debug("going to directory media: %s", content)
            files = os.listdir(content)
            files.sort()

            for file in files:
                abs_path = content + "/" + file
                player.play(abs_path, name)

                global jump
                if jump:
                    jump = False
                    break
        else:
            LOG.debug("`%s` is not a file nor a directory.", content)


def main():
    LOG.debug('main start with config_file %s nfs_local_path %s', config_file, nfs_local_path)

    # 1. get nfs list
    nfs_instance = nfs.Nfs(nfs_local_path, config_file)
    nfs_instance.mount()
    contents = nfs_instance.get_list()
    # LOG.debug(contents)

    # 2. update database
    m = media_list.MediaList(config_file)
    m.find_new_to_add(contents)

    # 3. bind hotkey
    hotkey.bind('q', hotkey_jump)

    # 4. Start web interface
    t2 = Thread(target=web_server)
    t2.start()

    # 5. Play
    play()


if __name__ == '__main__':
    main()

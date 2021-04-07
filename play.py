import os
import syslog
import random
import time
import getopt
import sys
import vlc
import functools
import termios
import tty
import media_list
import nfs
import logging

from pynput import keyboard
from flask import Flask
from threading import Thread

# @ -------- DEPENDENCY --------
"""
yum install kernel-headers-$(uname -r) -y
yum install gcc -y
yum install python-devel -y
yum install python3-pip -y
yum install python3-devel -y

pip3 install python-vlc pynput flask python-xlib system_hotkey prettytable pymysql sqlalchemy

yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm -y
yum install https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm -y
yum info vlc
yum install vlc -y

sed -i 's/geteuid/getppid/' /usr/bin/vlc
"""

# @ -------- LOGGING --------
logging.basicConfig(filename='/etc/jplayer/jplayer.log',
                    format='%(asctime)s %(name)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.DEBUG)
LOG = logging.getLogger(__name__)

# @ -------- GLOBAL --------
media_player = None
jump = False

# @ -------- CONFIG --------
# run_mode = 'local'
run_mode = 'remote'
directory = "/home/"
debug_mode = False
nfs_ip = "192.168.0.102"
nfs_dir = "/media/slot3_4t/media"
local_dir = "/home/pi/Desktop/nfs"

# @ -------- CONFIG end --------

# @ -------- HOTKEYS --------
# The key combination to check
COMBINATIONS = [
    {keyboard.Key.ctrl, keyboard.KeyCode(char='q')},
    {keyboard.Key.ctrl, keyboard.KeyCode(char='Q')}
]

# The currently active modifiers
current = set()


def execute():
    global media_player
    global jump
    jump = True
    media_player.stop()


def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()


def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)


def hotkey_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


# @ -------- RESTAPI --------
app = Flask(__name__)


@app.route('/')
def hello_world():
    return "hello world"


@app.route('/title/', methods=['GET'])
def rest_get_title():
    return str(media_player.get_title())


# curl --request POST 127.0.0.1:5000/next/
@app.route('/next/', methods=['POST'])
def rest_post_next():
    return str(media_player.stop())


def web_server():
    app.run()


# @ -------- WHAT --------
def _play(video):
    try:
        LOG.debug('playing media `%s`', video)

        global media_player
        global jump
        jump = False

        # creating Instance class object
        player = vlc.Instance()

        # creating a new media
        media = player.media_new(video)

        # creating a media player object
        media_player = player.media_player_new()

        media_player.set_media(media)

        media_player.set_video_title_display(3, 8000)

        media_player.set_fullscreen(True)

        # start playing video
        media_player.play()
        time.sleep(1)
        duration = 1000
        mv_length = media_player.get_length() - 1000
        LOG.debug(str(mv_length / 1000) + "s")

        while duration < mv_length:
            time.sleep(1)
            duration = duration + 1000
            status = media_player.get_state()

            # LOG.debug(status)
            if media_player.get_state() != vlc.State.Playing:
                media_player.stop()
                return

        media_player.stop()

    except Exception:
        LOG.error('got exception when playing %s', video, exc_info=True)

    return


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


def main():
    # start with config
    nfs_local_path = "/home/pi/Desktop/nfs"
    config_file = "./config.ini"
    LOG.debug('main start with config_file %s nfs_local_path %s', config_file, nfs_local_path)

    # 1. get nfs list
    nfs_instance = nfs.Nfs(nfs_local_path, config_file)
    nfs_instance.mount()
    contents = nfs_instance.get_list()
    LOG.debug(contents)

    # 2. update database
    m = media_list.MediaList(config_file)
    for content in contents:
        vid = m.get_id_by_path(content)
        if vid:
            pass
        else:
            m.create(path=content)

    list_all = m.get_list_all()
    m.show_info(list_all)

    # Get a random one
    # one = m.get_random()
    # LOG.debug('-'*30)
    # LOG.debug(one)

    # 3.5 Start hot_key listener
    t = Thread(target=hotkey_listener)
    t.start()

    # 3.6 Start web interface
    t2 = Thread(target=web_server)
    t2.start()

    # 4. Play
    while True:
        one = m.get_random()
        content = nfs_local_path + one

        if os.path.isfile(content):
            LOG.debug("going to play media: %s", content)
            _play(content)

        elif os.path.isdir(content):
            LOG.debug("going to directory media: %s", content)
            files = os.listdir(content)
            files.sort()

            for file in files:
                abs_path = content + "/" + file
                _play(abs_path)

                if jump:
                    break
        else:
            LOG.debug("`%s` is not a file nor a directory.", content)


if __name__ == '__main__':
    main()

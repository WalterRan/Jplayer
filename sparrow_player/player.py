"""player module"""

import time
import datetime
import vlc
from sparrow_player import logging_adaptor as logging

LOG = logging.get_logger(__name__)


SUPPORT_EXTENSION = (
    '.avi',
    '.mkv',
    '.mp4',
    '.rmvb',
    '.vob',
    '.mpg',
    '.m2v',
    '.mpeg',
    '.flv',
    '.ts',
    '.f4v',
    '.m4v',
    '.dat',
    '.asx'
)


class Player:
    """player class"""
    # Refs: https://blog.csdn.net/yingshukun/article/details/89527561
    def __init__(self):
        LOG.debug('Player init')
        instance = vlc.Instance()
        self.media = instance.media_player_new()
        self.uri = None

    def test(self):
        """test interface"""
        self.play('a.avi', title='testing', fullscreen=False)

    @staticmethod
    def support_file_type(media_full_path):
        if media_full_path.lower().endswith(SUPPORT_EXTENSION):
            return True

        return False

    def play(self, media_full_path, title=None, fullscreen=True):
        """play"""
        if media_full_path and self.support_file_type(media_full_path):
            if fullscreen:
                self.set_fullscreen()

            self.set_marquee()
            self.update_text(title)

            self.do_play(media_full_path)
            time.sleep(2)
            while self.is_playing():
                time.sleep(1)

        else:
            LOG.warning('cannot support the media file type: %s', media_full_path)

    def do_play(self, uri):
        """do play"""
        if uri:
            self.uri = uri
            self.media.set_mrl(uri)
            # self.add_callback(vlc.EventType.MediaPlayerEndReached, self.release)
            # self.add_callback(265, self.stop())
            self.media.play()
            time.sleep(1)
            LOG.debug('media %s total length %s', uri, self.get_length())

    def pause(self):
        """pause"""
        self.media.pause()

    def resume(self):
        """resume"""
        self.media.set_pause(0)

    def stop(self):
        """stop"""
        LOG.debug('stop is called')
        self.media.stop()

    # TODO: what is release
    def release(self):
        """release"""
        LOG.debug('release is called')
        return self.media.release()

    def is_playing(self):
        """is playing"""
        return self.media.is_playing()

    def get_time(self):
        """get time"""
        return self.media.get_time()

    # TODO: Cannot use
    def set_time(self):
        """set time"""
        return self.media.set_time()

    def get_length(self):
        """get length"""
        total_seconds = self.media.get_length() / 1000
        return str(datetime.timedelta(seconds=total_seconds))

    def get_state(self):
        """get state"""
        state = self.media.get_state()
        if state == vlc.State.Playing:
            return 1
        elif state == vlc.State.Paused:
            return 0

        return -1

    def get_position(self):
        """get position"""
        return self.media.get_position()

    def set_position(self, float_val):
        """set position"""
        return self.media.set_position(float_val)

    # TODO: Dont know how to use
    def set_ratio(self, ratio):
        """set ratio"""
        self.media.video_set_scale(0)
        self.media.video_set_aspect_ratio(ratio)

    # self.add_callback(vlc.EventType.MediaPlayerEndReached, self.release)
    def add_callback(self, event_type, callback):
        """add callback"""
        self.media.event_manager().event_attach(event_type, callback)

    def remove_callback(self, event_type, callback):
        """remove callback"""
        self.media.event_manager().event_detach(event_type, callback)

    def set_video_title_display(self):
        """set video title"""
        self.media.set_video_title_display(3, 8000)

    def set_fullscreen(self):
        """set fullscreen"""
        self.media.set_fullscreen(True)

    def get_uri(self):
        """get uri"""
        return self.uri

    def set_marquee(self):
        """set marquee"""
        self.media.video_set_marquee_int(vlc.VideoMarqueeOption.Enable, 1)
        self.media.video_set_marquee_int(vlc.VideoMarqueeOption.Size, 20)
        self.media.video_set_marquee_int(vlc.VideoMarqueeOption.Color, 0x44546A)
        # vlc.Position.top_right
        self.media.video_set_marquee_int(vlc.VideoMarqueeOption.Position, 6)
        self.media.video_set_marquee_int(vlc.VideoMarqueeOption.Timeout, 0)
        self.media.video_set_marquee_int(vlc.VideoMarqueeOption.Refresh, 10000)
        self.media.video_set_marquee_int(vlc.VideoMarqueeOption.Opacity, 180)

    def update_text(self, content):
        """update text"""
        try:
            LOG.debug('update title: %s', content)
            self.media.video_set_marquee_string(vlc.VideoMarqueeOption.Text, content)

        except Exception as e:
            LOG.exception('update_text exception: ', e)


player = Player()

if __name__ == '__main__':
    p = Player()
    p.test()

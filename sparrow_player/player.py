"""player module"""
import os
import time
import datetime
import vlc
import logging_adaptor as logging

LOG = logging.get_logger(__name__)


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

    def play(self, media, title=None, fullscreen=True):
        """play"""
        if media:
            if fullscreen:
                self.set_fullscreen()

            self.set_marquee()
            title = title or os.path.splitext(os.path.basename(media))[0]
            self.update_text(title)

            self.do_play(media)
            time.sleep(2)
            while self.is_playing():
                time.sleep(1)

    def do_play(self, uri):
        """do play"""
        if uri:
            self.uri = uri
            self.media.set_mrl(uri)
            # self.add_callback(vlc.EventType.MediaPlayerEndReached, self.release)
            # self.add_callback(265, self.stop())
            self.media.play()
            time.sleep(1)
            LOG.debug('media total length %s', self.get_length())

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
        self.media.video_set_marquee_string(vlc.VideoMarqueeOption.Text, content)


player = Player()

if __name__ == '__main__':
    p = Player()
    p.test()

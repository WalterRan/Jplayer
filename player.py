import logging_adaptor as logging

import os
import vlc
import time

LOG = logging.getLogger(__name__)


class Player:
    # Refs: https://blog.csdn.net/yingshukun/article/details/89527561
    def __init__(self):
        LOG.debug('Player init')
        instance = vlc.Instance()
        self.media = instance.media_player_new()
        self.uri = None

    def test(self):
        self.play('a.avi')

    def play(self, media, title=None):
        if media:
            self.set_fullscreen()
            self.set_marquee()
            title = title or os.path.splitext(os.path.basename(media))[0]
            self.update_text(title)

            self.do_play(media)
            time.sleep(2)
            while self.is_playing():
                time.sleep(1)

    def do_play(self, uri):
        if uri:
            self.uri = uri
            self.media.set_mrl(uri)
            LOG.debug('%s', str(self.media.get_length()))
            # self.add_callback(vlc.EventType.MediaPlayerEndReached, self.release)
            # self.add_callback(265, self.stop())
            return self.media.play()

    def pause(self):
        self.media.pause()

    def resume(self):
        self.media.set_pause(0)

    def stop(self):
        LOG.debug('stop is called')
        self.media.stop()

    # TODO: what is release
    def release(self):
        LOG.debug('release is called')
        return self.media.release()

    def is_playing(self):
        return self.media.is_playing()

    def get_time(self):
        return self.media.get_time()

    # TODO: Cannot use
    def set_time(self):
        return self.media.set_time()

    def get_length(self):
        return self.media.get_length()

    def get_state(self):
        state = self.media.get_state()
        if state == vlc.State.Playing:
            return 1
        elif state == vlc.State.Paused:
            return 0
        else:
            return -1

    def get_position(self):
        return self.media.get_position()

    def set_position(self, float_val):
        return self.media.set_position(float_val)

    # TODO: Dont know how to use
    def set_ratio(self, ratio):
        self.media.video_set_scale(0)
        self.media.video_set_aspect_ratio(ratio)

    # self.add_callback(vlc.EventType.MediaPlayerEndReached, self.release)
    def add_callback(self, event_type, callback):
        self.media.event_manager().event_attach(event_type, callback)

    def remove_callback(self, event_type, callback):
        self.media.event_manager().event_detach(event_type, callback)

    def set_video_title_display(self):
        self.media.set_video_title_display(3, 8000)

    def set_fullscreen(self):
        self.media.set_fullscreen(True)

    def get_uri(self):
        return self.uri

    def set_marquee(self):
        self.media.video_set_marquee_int(vlc.VideoMarqueeOption.Enable, 1)
        self.media.video_set_marquee_int(vlc.VideoMarqueeOption.Size, 20)
        self.media.video_set_marquee_int(vlc.VideoMarqueeOption.Color, 0x44546A)
        # vlc.Position.top_right
        self.media.video_set_marquee_int(vlc.VideoMarqueeOption.Position, 6)
        self.media.video_set_marquee_int(vlc.VideoMarqueeOption.Timeout, 0)
        self.media.video_set_marquee_int(vlc.VideoMarqueeOption.Refresh, 10000)
        self.media.video_set_marquee_int(vlc.VideoMarqueeOption.Opacity, 180)

    def update_text(self, content):
        self.media.video_set_marquee_string(vlc.VideoMarqueeOption.Text, content)


player = Player()

if __name__ == '__main__':
    p = Player()
    p.test()


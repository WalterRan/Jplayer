from pynput import keyboard
from threading import Thread
import logging_adaptor as logging


LOG = logging.getLogger(__name__)


class HotKey(object):
    def __init__(self):
        LOG.debug('HotKey init')
        self.t = None

    def bind(self, hot_key, func):
        current = set()

        if hot_key.isalpha():
            COMBINATIONS = [
                {keyboard.Key.ctrl, keyboard.KeyCode(char=hot_key.lower())},
                {keyboard.Key.ctrl, keyboard.KeyCode(char=hot_key.upper())}
            ]

        def on_press(key):
            if any([key in COMBO for COMBO in COMBINATIONS]):
                current.add(key)
                if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
                    func()

        def on_release(key):
            if any([key in COMBO for COMBO in COMBINATIONS]):
                current.remove(key)

        def hotkey_listener():
            with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()

        self.t = Thread(target=hotkey_listener)
        self.t.start()


hotkey = HotKey()


if __name__ == '__main__':
    pass

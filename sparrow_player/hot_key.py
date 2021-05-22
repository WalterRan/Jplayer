"""This module bind hot key to a callback function"""
from threading import Thread

from pynput import keyboard

import logging_adaptor as logging


LOG = logging.get_logger(__name__)


class HotKey:
    """
    Define the hotkey bind
    """
    def __init__(self):
        LOG.debug('HotKey init')
        self.hot_key_thread = None
        self.current = set()
        self.func = None
        self.combinations = None

    def bind(self, hot_key, func):
        """
        Bind a hot key to function callback
        """
        self.func = func

        if hot_key.isalpha():
            self.combinations = [
                {keyboard.Key.ctrl, keyboard.KeyCode(char=hot_key.lower())},
                {keyboard.Key.ctrl, keyboard.KeyCode(char=hot_key.upper())}
            ]

        self.hot_key_thread = Thread(target=self.hotkey_listener)
        self.hot_key_thread.start()

    def on_press(self, key):
        """
        on_press
        """
        if any([key in COMBO for COMBO in self.combinations]):
            self.current.add(key)
            if any(all(k in self.current for k in COMBO) for COMBO in self.combinations):
                self.func()

    def on_release(self, key):
        """
        on_release
        """
        if any([key in COMBO for COMBO in self.combinations]):
            self.current.remove(key)

    def hotkey_listener(self):
        """
        hotkey_listener
        """
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()


if __name__ == '__main__':
    pass

# -*- coding: utf-8 -*-

import unittest
import random
import sys
sys.path.append(".")

from sparrow_player.player import Player


class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        self.player = Player()

    def tearDown(self):
        pass

    def test_get_id_by_path(self):
        should_support = [
            '/home/media/The.Shawshank.Redemption.mkv',
            'a.avi',
            'b.mkv'
        ]

        not_support = [
            'as.torrent'
        ]

        for one in should_support:
            self.assertTrue(self.player.support_file_type(one))

        for one in not_support:
            self.assertFalse(self.player.support_file_type(one))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DatabaseTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)

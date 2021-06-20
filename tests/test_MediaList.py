# -*- coding: utf-8 -*-

import unittest
import random
import sys
sys.path.append(".")

from sparrow_player.media_list import MediaList


class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        self.media_list = MediaList('127.0.0.1', 'root', 'ut')
        self.media_list.delete_all()

        self.media_list.add('/home/media/The.Shawshank.Redemption.mkv',
                            simple_name='肖生克的救赎', origin_name='The Shawshank Redemption', year='1994')

        self.media_list.add('/home/media/The.Godfather.avi',
                            simple_name='教父', origin_name='The Godfather', year='1972')

        self.media_list.add('/home/media/simple-name-only.mp4',
                            simple_name='the simple name', year='2000')

        self.media_list.add('/home/media/origin-name-only.mp4',
                            origin_name='the origin name', year='2000')

        self.media_list.add('/home/media/neither-origin-simple-name.mp4',
                            year='2000')

    def tearDown(self):
        self.media_list.delete_all()
        self.media_list.remove()

    def test_get_id_by_path(self):
        response = self.media_list.get_id_by_path('/home/media/The.Shawshank.Redemption.mkv')
        is_int = isinstance(response, int)
        self.assertTrue(is_int)

    def test_delete_by_id(self):
        media_id = self.media_list.get_id_by_path('/home/media/The.Shawshank.Redemption.mkv')
        self.media_list.delete_by_id(media_id)
        m_id = self.media_list.get_id_by_path('/home/media/The.Shawshank.Redemption.mkv')
        self.assertIsNone(m_id)

    def test_get_name(self):
        """
        Try to add the full 3 * 3 mitrix next time :)
        | origin-name | simple-name | year |
        """
        # origin-name | simple-name | year
        self.assertEqual(
            self.media_list.get_name_by_path('/home/media/The.Shawshank.Redemption.mkv'),
            'The Shawshank Redemption.肖生克的救赎.1994'
        )

        # no origin-name | simple-name | year
        self.assertEqual(
            self.media_list.get_name_by_path('/home/media/simple-name-only.mp4'),
            'the simple name.2000'
        )

        # origin-name | no simple-name | year
        self.assertEqual(
            self.media_list.get_name_by_path('/home/media/origin-name-only.mp4'),
            'the origin name.2000'
        )

        # no origin-name | no simple-name | no year
        self.assertEqual(
            self.media_list.get_name_by_path('/home/media/neither-origin-simple-name.mp4'),
            'neither-origin-simple-name'
        )

    def test_update_path(self):
        media_id = self.media_list.get_random_media_id()
        modify_path = 'the test path string'

        self.media_list.update_path(media_id, modify_path)
        get_media = self.media_list.get_by_id(media_id)
        self.assertEqual(get_media.path, modify_path)

    def test_update_priority(self):
        media_id = self.media_list.get_random_media_id()
        modify_priority = 100

        self.media_list.update_priority(media_id, modify_priority)
        get_media = self.media_list.get_by_id(media_id)
        self.assertEqual(get_media.play_info.priority, modify_priority)

    def test_increase_count(self):
        random_limit = 100

        media_id = self.media_list.get_random_media_id()
        media = self.media_list.get_by_id(media_id)

        # test played count
        random_increase = random.randint(0, random_limit)
        except_played_count = media.play_info.played + random_increase
        for i in range(random_increase):
            self.media_list.increase_played(media_id)

        # test finished count
        random_increase = random.randint(0, random_limit)
        except_finished_count = media.play_info.finished + random_increase
        for i in range(random_increase):
            self.media_list.increase_finished(media_id)

        # test jumped count
        random_increase = random.randint(0, random_limit)
        except_jumped_count = media.play_info.jumped + random_increase
        for i in range(random_increase):
            self.media_list.increase_jumped(media_id)

        get_media = self.media_list.get_by_id(media.id)
        self.assertEqual(get_media.play_info.played, except_played_count)
        self.assertEqual(get_media.play_info.finished, except_finished_count)
        self.assertEqual(get_media.play_info.jumped, except_jumped_count)

    def test_update_media_info(self):
        media_id = self.media_list.get_random_media_id()
        modify_simple_name = 'the test simple name'
        modify_origin_name = 'the test origin name'
        modify_year = '1984'

        self.media_list.update_simple_name(media_id, modify_simple_name)
        self.media_list.update_origin_name(media_id, modify_origin_name)
        self.media_list.update_year(media_id, modify_year)

        media = self.media_list.get_by_id(media_id)
        self.assertEqual(media.media_info.simple_name, modify_simple_name)
        self.assertEqual(media.media_info.origin_name, modify_origin_name)
        self.assertEqual(media.media_info.year, modify_year)

    def test_get_random_media_path(self):
        s = set()
        for i in range(100):
            random_media_path = self.media_list.get_random_media_path()
            self.assertEqual(type(random_media_path), str)
            s.add(random_media_path)

        self.assertEqual(len(s), 5)

    def test_find_new_to_add(self):
        path = list()
        path.append('/home/media/The.Shawshank.Redemption.mkv')
        path.append('/home/media/The.Godfather.avi')
        path.append('/home/media/simple-name-only.mp4')
        path.append('/home/media/origin-name-only.mp4')
        path.append('/home/media/neither-origin-simple-name.mp4')

        path.append('new_test_path_1')
        path.append('new_test_path_2')

        self.media_list.find_new_to_add(path)
        count = self.media_list.get_medias_count()
        self.assertEqual(count, len(path))

    @unittest.skip("Waiting for new add function :)")
    def test_add(self):
        self.media_list.add('/home/media/The.Shawshank.Redemption.mkv',
                            simple_name='肖生克的救赎', origin_name='The Shawshank Redemption', year='1994')


if __name__ == '__main__':
    suite = unittest.TestSuite()
    # suite.addTest(DatabaseTestCase('test_add'))

    suite = unittest.TestLoader().loadTestsFromTestCase(DatabaseTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)

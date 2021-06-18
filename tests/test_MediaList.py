# -*- coding: utf-8 -*-

import unittest
import sys
sys.path.append("/home/src/sparrow-player")
sys.path.append("/home/src/sparrow-player/sparrow_player")


from sparrow_player.media_list import MediaList


class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        self.session = MediaList('127.0.0.1', 'root', 'ut')
        self.session.delete_all()

        self.session.add('/home/media/The.Shawshank.Redemption.mkv',
                         simple_name='肖生克的救赎', origin_name='The Shawshank Redemption', year='1994')

        self.session.add('/home/media/The.Godfather.avi',
                         simple_name='教父', origin_name='The Godfather', year='1972')

        self.session.add('/home/media/huayangnianhua.mp4',
                         simple_name='花样年华', origin_name='', year='2000')

    def tearDown(self):
        self.session.delete_all()
        self.session.remove()

    def test_connection(self):
        pass

    def test_get_id_by_path(self):
        response = self.session.get_id_by_path('/home/media/The.Shawshank.Redemption.mkv')
        is_int = isinstance(response, int)
        self.assertTrue(is_int)

    def test_delete_by_id(self):
        media_id = self.session.get_id_by_path('/home/media/The.Shawshank.Redemption.mkv')
        self.session.delete_by_id(media_id)
        m_id = self.session.get_id_by_path('/home/media/The.Shawshank.Redemption.mkv')
        self.assertIsNone(m_id)

    def test_get_name_by_path(self):
        name = self.session.get_name_by_path('/home/media/The.Shawshank.Redemption.mkv')
        self.assertEqual(name, 'The Shawshank Redemption.肖生克的救赎.1994')

    def test_get_name_by_path_without_origin_name(self):
        # name = self.session.get_name_by_path('/home/media/huayangnianhua.mp4')
        name = self.session.get_name_by_path('/home/media/huayangnianhua.mp4')
        self.assertEqual(name, '花样年华.2000')

    def test_update_path(self):
        medias = self.session.get_all()
        media = medias[0]
        modify_path = 'the test path string'

        self.session.update_path(media.id, modify_path)
        get_media = self.session.get_by_id(media.id)
        self.assertEqual(get_media.path, modify_path)

    def test_update_priority(self):
        medias = self.session.get_all()
        media = medias[0]
        modify_priority = 100

        self.session.update_priority(media.id, modify_priority)
        get_media = self.session.get_by_id(media.id)
        self.assertEqual(get_media.play_info.priority, modify_priority)

    def test_update_played(self):
        return

        medias = self.session.get_all()
        media = medias[0]
        except_played_count = media.play_info.played + 1

        self.session.increase_played(media.id)
        get_media = self.session.get_by_id(media.id)
        self.assertEqual(get_media.play_info.played, except_played_count)

    def test_update_finished(self):
        pass

    def test_update_jumped(self):
        pass

    def test_update_simple_name(self):
        medias = self.session.get_all()
        media = medias[0]
        modify_simple_name = 'the test simple name'

        self.session.update_simple_name(media.id, modify_simple_name)
        get_media = self.session.get_by_id(media.id)
        self.assertEqual(get_media.media_info.simple_name, modify_simple_name)

    def test_update_origin_name(self):
        medias = self.session.get_all()
        media = medias[0]
        modify_origin_name = 'the test origin name'

        self.session.update_origin_name(media.id, modify_origin_name)
        get_media = self.session.get_by_id(media.id)
        self.assertEqual(get_media.media_info.origin_name, modify_origin_name)

    def test_update_year(self):
        medias = self.session.get_all()
        media = medias[0]
        modify_year = '1984'

        self.session.update_year(media.id, modify_year)
        get_media = self.session.get_by_id(media.id)
        self.assertEqual(get_media.media_info.year, modify_year)

    def test_get_random_new(self):
        self.session.get_random_new()


if __name__ == '__main__':
    suite = unittest.TestSuite()
    # suite.addTest(DatabaseTestCase('test_connection'))n
    # suite.addTest(DatabaseTestCase('test_get_id_by_path'))
    # suite.addTest(DatabaseTestCase('test_get_name_by_path_without_origin_name'))
    suite.addTest(DatabaseTestCase('test_get_random_new'))

    # suite = unittest.TestLoader().loadTestsFromTestCase(DatabaseTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)

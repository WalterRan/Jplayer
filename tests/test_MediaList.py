# -*- coding: utf-8 -*-

import unittest
import sys
sys.path.append("/home/src/sparrow-player")
sys.path.append("/home/src/sparrow-player/sparrow_player")


from sparrow_player.media_list import MediaList


class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        self.session = MediaList('127.0.0.1', 'root', 'ut')

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
        name = self.session.get_name_by_path('/home/media/huayangnianhua.mp4')
        print(name)
        self.assertEqual(name, 'The Shawshank Redemption.肖生克的救赎.1994')


if __name__ == '__main__':
    suite = unittest.TestSuite()
    # suite.addTest(DatabaseTestCase('test_connection'))n
    # suite.addTest(DatabaseTestCase('test_get_id_by_path'))

    suite = unittest.TestLoader().loadTestsFromTestCase(DatabaseTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)

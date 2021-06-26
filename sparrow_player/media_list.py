"""media list"""
import os
import random

import sys
from os.path import abspath, dirname
sys.path.append(dirname(dirname(abspath(__file__))))

import utils
from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import exc
from prettytable import PrettyTable
from models.media_list import BaseInfo
from models.media_list import PlayInfo
from models.media_list import MediaInfo
from sparrow_player import logging_adaptor as logging


LOG = logging.get_logger(__name__)
Base = declarative_base()


DEFAULT_PRIORITY = 5


class MediaList(object):
    """media list class"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            LOG.debug('Creating the `MediaList` object')
            cls._instance = super(MediaList, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

    # TODO: the only use of these parameters is for unit test, should try to remove them next time.
    def __init__(self, server_ip=None, username=None, db_name=None):
        if not (server_ip and username and db_name):
            config_file = utils.get_config_file()
            db_config = ConfigParser()
            db_config.read(config_file)

            db_config = db_config.__getitem__('database')

            server_ip = db_config.get('ip')
            username = db_config.get('username')
            db_name = db_config.get('db_name')

        connection = 'mysql+pymysql://' + username + '@' + server_ip + '/' + db_name
        LOG.debug('connection = %s', connection)
        engine = create_engine(connection, pool_recycle=3600)
        db_session = sessionmaker(bind=engine)
        self.session = db_session()

    def remove(self):
        self.session.close()

    def add(self, path, simple_name='', origin_name='', year=''):
        with self.session.begin(subtransactions=True):
            media = BaseInfo(path=path)
            media.play_info = PlayInfo(priority=DEFAULT_PRIORITY, played=0, finished=0, jumped=0)
            media.media_info = MediaInfo(simple_name=simple_name, origin_name=origin_name, year=year)

            self.session.add(media)

    def get_by_id(self, media_id):
        try:
            return self.session.query(BaseInfo).filter_by(id=media_id).one()

        except exc.NoResultFound as e:
            LOG.debug('no result found %s', e)
            return

        except exc.MultipleResultsFound as e:
            LOG.debug('Error: ', e)
            print('Error: ', e)
            return None

    def get_id_by_path(self, media_path):
        """get id by path"""
        media = self.session.query(BaseInfo).filter_by(path=media_path).one_or_none()

        if media:
            return media.id

        return None

    def delete_by_id(self, media_id):
        """delete by id"""
        with self.session.begin(subtransactions=True):
            self.session.query(BaseInfo).filter_by(id=media_id).delete()

    def delete_all(self):
        """delete all for unit test"""
        with self.session.begin(subtransactions=True):
            self.session.query(MediaInfo).delete()
            self.session.query(PlayInfo).delete()
            self.session.query(BaseInfo).delete()

    # should called get title by path
    def get_media_title_by_path(self, media_path):
        """get name by path"""
        try:
            media = self.session.query(BaseInfo).filter_by(path=media_path).one()

            '''
            sep = '.'
            full_name = [media.media_info.origin_name,
                         media.media_info.simple_name,
                         media.media_info.year]

            not_none_name = [str(full_name).strip() for f in full_name if f]
            return sep.join(not_none_name)
            '''

            name = str()
            if media.media_info.origin_name:
                name += media.media_info.origin_name

            if media.media_info.simple_name:
                if name:
                    name += '.'
                name += media.media_info.simple_name

            if not name:
                return os.path.splitext(os.path.basename(media_path))[0]

            if media.media_info.year:
                if name:
                    name += '.'
                name += media.media_info.year

            return name

        except exc.NoResultFound as e:
            LOG.debug('no result found %s', e)
            return

        except exc.MultipleResultsFound as e:
            LOG.debug('Error: ', e)
            print('Error: ', e)
            return None

    def _update(self, media_id,
                path=None,
                priority=None,
                simple_name=None, origin_name=None, year=None):
        """update"""
        try:
            with self.session.begin(subtransactions=True):
                media = self.session.query(BaseInfo).filter_by(id=media_id).one()

                if path:
                    media.path = path

                if priority:
                    media.play_info.priority = priority

                if simple_name:
                    media.media_info.simple_name = simple_name

                if origin_name:
                    media.media_info.origin_name = origin_name

                if year:
                    media.media_info.year = year

            # why need this?
            self.session.commit()

        except exc.NoResultFound as e:
            LOG.debug('no result found %s', e)
            return

        except exc.MultipleResultsFound as e:
            LOG.debug('Error: ', e)
            print('Error: ', e)
            return None

    def update_path(self, media_id, path):
        self._update(media_id, path=path)

    def update_priority(self, media_id, priority):
        self._update(media_id, priority=priority)

    def update_simple_name(self, media_id, simple_name):
        self._update(media_id, simple_name=simple_name)

    def update_origin_name(self, media_id, origin_name):
        self._update(media_id, origin_name=origin_name)

    def update_year(self, media_id, year):
        self._update(media_id, year=year)

    def increase_played(self, media_id):
        play_info = self.session.query(PlayInfo).filter_by(media_id=media_id).one()
        play_info.played += 1
        self.session.commit()

    def increase_finished(self, media_id):
        play_info = self.session.query(PlayInfo).filter_by(media_id=media_id).one()
        play_info.finished += 1
        self.session.commit()

    def increase_jumped(self, media_id):
        play_info = self.session.query(PlayInfo).filter_by(media_id=media_id).one()
        play_info.jumped += 1
        self.session.commit()

    @staticmethod
    def show_info(medias):
        """show info"""
        table = PrettyTable(['id', 'path',
                             'priority', 'played', 'finished', 'jumped',
                             'simple_name', 'origin_name', 'year'])
        for media in medias:
            table.add_row([
                media.id,
                media.path,
                media.play_info.priority,
                media.play_info.played,
                media.play_info.finished,
                media.play_info.jumped,
                media.media_info.simple_name,
                media.media_info.origin_name,
                media.media_info.year,
            ])
        LOG.debug(table)

    def get_random_media_id(self):
        medias = self.session.query(BaseInfo.id, PlayInfo.priority).join(PlayInfo).all()

        all_media = []
        for media in medias:
            for i in range(media.priority):
                all_media.append(media.id)
        LOG.debug('unfold media %d to medias %d', len(medias), len(all_media))

        random_index = random.randint(0, len(all_media)-1)

        return all_media[random_index]

    def get_random_media_path(self):
        random_select = self.get_random_media_id()

        random_media_path = self.session.query(BaseInfo.path)\
            .filter_by(id=random_select)\
            .one()

        LOG.debug('pick a random one `%s`, NO: %d', random_media_path, random_select)

        return str(getattr(random_media_path, 'path'))

    def find_new_to_add(self, contents):
        """find new to add"""
        for content in contents:
            media_id = self.get_id_by_path(content)
            if media_id:
                pass
            else:
                self.add(path=content)

    def get_medias_count(self):
        return self.session.query(BaseInfo).count()


def main():
    import pdb; pdb.set_trace()
    # a.MediaList('127.0.0.1', 'root', 'sparrow_player')


if __name__ == '__main__':
    main()

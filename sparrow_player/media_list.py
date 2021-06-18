"""media list"""
import sys
sys.path.append("/home/src/sparrow-player")
sys.path.append("/home/src/sparrow-player/sparrow_player")

import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import exc
from prettytable import PrettyTable
from models.media_list import BaseInfo
from models.media_list import PlayInfo
from models.media_list import MediaInfo
import logging_adaptor as logging


LOG = logging.get_logger(__name__)
Base = declarative_base()


DEFAULT_PRIORITY = 5


class MediaList:
    """media list class"""

    def __init__(self, server_ip, username, db_name):
        LOG.debug('MediaList init start')

        connection = 'mysql+pymysql://' + username + '@' + server_ip + '/' + db_name
        LOG.debug('connection = %s', connection)
        engine = create_engine(connection, pool_recycle=3600)
        db_session = sessionmaker(bind=engine)
        self.session = db_session()

    def remove(self):
        self.session.close()
        # self.session.close_all()

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
    def get_name_by_path(self, media_path):
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

    # TODO modify to get_random_one by priority
    def get_all(self):
        """get all medias"""
        return self.session.query(BaseInfo).all()

    def update(self, media_id,
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

        except exc.NoResultFound as e:
            LOG.debug('no result found %s', e)
            return

        except exc.MultipleResultsFound as e:
            LOG.debug('Error: ', e)
            print('Error: ', e)
            return None

    def update_path(self, media_id, path):
        self.update(media_id, path=path)

    def update_priority(self, media_id, priority):
        self.update(media_id, priority=priority)

    def update_simple_name(self, media_id, simple_name):
        self.update(media_id, simple_name=simple_name)

    def update_origin_name(self, media_id, origin_name):
        self.update(media_id, origin_name=origin_name)

    def update_year(self, media_id, year):
        self.update(media_id, year=year)

    def increase_played(self, media_id):
        with self.session.begin(subtransactions=True):
            media = self.session.query(BaseInfo).filter_by(id=media_id).one
            import pdb; pdb.set_trace()
            media.play_info.played += 1

    def increase_finished(self, media_id):
        with self.session.begin(subtransactions=True):
            media = self.session.query(BaseInfo).filter_by(id=media_id).one
            media.play_info.finished += 1

    def increase_jumped(self, media_id):
        with self.session.begin(subtransactions=True):
            media = self.session.query(BaseInfo).filter_by(id=media_id).one
            media.play_info.jumped += 1

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

    def unfold_by_priority(self):
        medias = self.session.query(BaseInfo).all()
        print(medias)

    def get_random_new(self):
        self.unfold_by_priority()

    def get_random(self):
        """get random"""
        medias = self.get_all()

        all_media = []
        for media in medias:
            for i in range(media.play_info.priority):
                all_media.append(media.path)

        LOG.debug('unfold media %d to medias %d', len(medias), len(all_media))
        random_select = random.randint(0, len(all_media))
        LOG.debug('pick a random one `%s`', all_media[random_select])

        return all_media[random_select]

    def find_new_to_add(self, contents):
        """find new to add"""
        for content in contents:
            media_id = self.get_id_by_path(content)
            if media_id:
                pass
            else:
                self.add(path=content)

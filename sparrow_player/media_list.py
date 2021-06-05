"""media list"""
import random
from configparser import ConfigParser

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
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

        # cfg = ConfigParser()
        # cfg.read(config_file)

        # db_config = cfg.__getitem__('database')

        # server_ip = db_config.get('ip')
        # username = db_config.get('username')
        # db_name = db_config.get('db_name')
        # password = cs.get('password')

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

    def get_id_by_path(self, media_path):
        """get id by path"""
        media = self.session.query(BaseInfo).filter_by(path=media_path).one_or_none()

        if media:
            return media.id

        return None

    def delete_by_id(self, media_id):
        """delete by id"""
        media = self.session.query(BaseInfo).filter_by(id=media_id).one_or_none()
        if media:
            self.session.delete(media)
            self.session.commit()
        else:
            raise

    def delete_all(self):
        """delete all for unit test"""
        with self.session.begin(subtransactions=True):
            self.session.query(BaseInfo).delete()

    # should called get title by path
    def get_name_by_path(self, media_path):
        """get name by path"""
        media = self.session.query(BaseInfo).filter_by(path=media_path).one_or_none()
        if media:
            origin_name = media.media_info.origin_name + '.' if media.media_info.origin_name is not None else ''
            return origin_name + media.media_info.simple_name + '.' + media.media_info.year

        return None

    # TODO modify to get_random_one by priority
    def get_list_all(self):
        """get list all"""
        list_all = self.session.query(BaseInfo).all()

        return list_all

    def update(self, vid, name=None, priority=None, played=None, failed=None, jumped=None):
        """update"""
        media = self.session.query(MediaListDB).filter_by(id=vid).one_or_none()
        if media:
            if name:
                media.name = name
            if priority:
                media.priority = priority

            if played:
                media.played = played

            if failed:
                media.failed = failed

            if jumped:
                media.jumped = jumped

            self.session.commit()

    def update_name(self, vid, name):
        """update_name"""
        self.update(vid, name=name)

    def update_priority(self, media_id, action='add'):
        """update priortity"""
        media = self.session.query(PlayInfo).filter_by(media_id=media_id).one_or_none()
        if media:
            raw_priority = media.priority

            if action == 'add':
                priority = raw_priority + 1
            else:
                if raw_priority > 0:
                    priority = raw_priority - 1
                else:
                    priority = 0
            self.update(media_id, priority=priority)
        else:
            raise

    def increase_fail_count(self, media_id):
        """increate_fail_count"""
        media = self.session.query(PlayInfo).filter_by(media_id=media_id).one_or_none()
        if media:
            self.update(media_id, failed=media.failed + 1)
        else:
            raise

    def increase_play_count(self, media_id):
        """increate play count"""
        media = self.session.query(PlayInfo).filter_by(media_id=media_id).one_or_none()
        if media:
            self.update(media_id, played=media.played + 1)
        else:
            raise

    def increase_jump_count(self, media_id):
        """increase jump count"""
        media = self.session.query(PlayInfo).filter_by(media_id=media_id).one_or_none()
        if media:
            self.update(media_id, jumped=media.jumped + 1)
        else:
            raise

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

    def get_random(self):
        """get random"""
        medias = self.get_list_all()

        all_media = []
        for media in medias:
            for i in range(media.priority):
                all_media.append(media.path)

        LOG.debug('unfold media %d to medias %d', len(medias), len(all_media))
        random_select = random.randint(0, len(all_media))
        LOG.debug('pick a random one `%s`', all_media[random_select])

        return all_media[random_select]

    def find_new_to_add(self, contents):
        """find new to add"""
        for content in contents:
            vid = self.get_id_by_path(content)
            if vid:
                pass
            else:
                self.add(path=content)

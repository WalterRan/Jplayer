"""media list"""
import random
from configparser import ConfigParser

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from prettytable import PrettyTable

import logging_adaptor as logging

LOG = logging.get_logger(__name__)
# sa.Column, sa.String, sa.create_engine
Base = declarative_base()


class MediaListDB(Base):
    """media list base class"""
    __table_args__ = {'mysql_engine': 'InnoDB'}
    __table_initialized__ = False
    __tablename__ = 'media_list'

    id = sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, primary_key=True)
    name = sa.Column(sa.String(255), nullable=True)
    path = sa.Column(sa.String(255), nullable=False)
    priority = sa.Column('priority', sa.Integer(), nullable=False)
    played = sa.Column('played', sa.Integer(), nullable=False)
    failed = sa.Column('failed', sa.Integer(), nullable=False)
    jumped = sa.Column('jumped', sa.Integer(), nullable=False)


class MediaList:
    """media list class"""

    def __init__(self, config_file):
        LOG.debug('MediaList init start')

        cfg = ConfigParser()
        cfg.read(config_file)

        db_config = cfg.__getitem__('database')

        server_ip = db_config.get('ip')
        username = db_config.get('username')
        db_name = db_config.get('db_name')
        # password = cs.get('password')

        connection = 'mysql+pymysql://' + username + '@' + server_ip + '/' + db_name
        LOG.debug('connection = %s', connection)
        engine = create_engine(connection, pool_recycle=3600)
        db_session = sessionmaker(bind=engine)
        self.session = db_session()

    def get_list_all(self):
        """get list all"""
        list_all = self.session.query(MediaListDB).all()

        return list_all

    def get_id_by_path(self, media_path):
        """get id by path"""
        media = self.session.query(MediaListDB).filter_by(path=media_path).one_or_none()

        if media:
            return media.id

        return None

    def create(self, path, name=None):
        """create"""
        new_list = MediaListDB(path=path, name=name, priority=5, played=0, failed=0, jumped=0)
        self.session.add(new_list)
        self.session.commit()

    def delete_by_id(self, vid):
        """delete by id"""
        media = self.session.query(MediaListDB).filter_by(id=vid).one_or_none()
        if media:
            self.session.delete(media)
            self.session.commit()

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

    def update_priority(self, vid, action='add'):
        """update priortity"""
        media = self.session.query(MediaListDB).filter_by(id=vid).one_or_none()
        if media:
            raw_priority = media.priority

            if action == 'add':
                priority = raw_priority + 1
            else:
                if raw_priority > 0:
                    priority = raw_priority - 1
                else:
                    priority = 0
            self.update(vid, priority=priority)

    def increase_fail_count(self, vid):
        """increate_fail_count"""
        media = self.session.query(MediaListDB).filter_by(id=vid).one_or_none()
        if media:
            self.update(vid, failed=media.failed + 1)

    def increase_play_count(self, vid):
        """increate play count"""
        media = self.session.query(MediaListDB).filter_by(id=vid).one_or_none()
        if media:
            self.update(vid, played=media.played + 1)

    def increase_jump_count(self, vid):
        """increase jump count"""
        media = self.session.query(MediaListDB).filter_by(id=vid).one_or_none()
        if media:
            self.update(vid, jumped=media.jumped + 1)

    @staticmethod
    def show_info(medias):
        """show info"""
        table = PrettyTable(['id', 'name', 'priority', 'played', 'failed', 'jumped', 'path'])
        for media in medias:
            table.add_row([
                media.id,
                media.name,
                media.priority,
                media.played,
                media.failed,
                media.jumped,
                media.path[:70],
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

    def get_name_by_path(self, media_path):
        """get name by path"""
        media = self.session.query(MediaListDB).filter_by(path=media_path).one_or_none()
        if media:
            return media.name

        return None

    def find_new_to_add(self, contents):
        """find new to add"""
        for content in contents:
            vid = self.get_id_by_path(content)
            if vid:
                pass
            else:
                self.create(path=content)

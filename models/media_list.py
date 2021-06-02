from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()

"""
create database sparrow_player;
"""

class BaseInfo(Base):
    """
    Media into database
    change the info to a short name
    """
    __table_args__ = {'mysql_engine': 'InnoDB'}
    __table_initialized__ = False
    __tablename__ = 'base_info'

    mysql_character_set = 'utf8'

    id = Column('id', Integer(), autoincrement=True, nullable=False, primary_key=True)
    path = Column(String(255), nullable=False)
    play_info = relationship("PlayInfo", uselist=False, back_populates="base_info")
    media_info = relationship("MediaInfo", uselist=False, back_populates="base_info")


class PlayInfo(Base):
    """
    Media list database model
    Record the information about playing
    """
    __table_args__ = {'mysql_engine': 'InnoDB'}
    __table_initialized__ = False
    __tablename__ = 'play_info'

    mysql_character_set = 'utf8'

    id = Column('id', Integer(), autoincrement=True, nullable=False, primary_key=True)
    priority = Column('priority', Integer(), nullable=False)
    played = Column('played', Integer(), nullable=False)
    finished = Column('finished', Integer(), nullable=False)
    jumped = Column('jumped', Integer(), nullable=False)

    media_id = Column(Integer, ForeignKey('base_info.id'))
    base_info = relationship("BaseInfo", back_populates="play_info")


class MediaInfo(Base):
    """
    Media into database
    Record the information about media
    """
    __table_args__ = {'mysql_engine': 'InnoDB'}
    __table_initialized__ = False
    __tablename__ = 'media_info'

    mysql_character_set = 'utf8'

    id = Column('id', Integer(), autoincrement=True, nullable=False, primary_key=True)
    simple_name = Column(String(255), nullable=True)
    origin_name = Column(String(255), nullable=True)
    year = Column(String(8), nullable=True)
    media_id = Column(Integer, ForeignKey('base_info.id'))
    base_info = relationship("BaseInfo", back_populates="media_info")

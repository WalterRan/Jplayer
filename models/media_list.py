from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

"""
create database sparrow_player;
"""

class MediaListDB(Base):
    __table_args__ = {'mysql_engine': 'InnoDB'}
    __table_initialized__ = False
    __tablename__ = 'media_list'

    mysql_character_set = 'utf8'

    id = Column('id', Integer(), autoincrement=True, nullable=False, primary_key=True)
    name = Column(String(255), nullable=True)
    path = Column(String(255), nullable=False)
    priority = Column('priority', Integer(), nullable=False)
    played = Column('played', Integer(), nullable=False)
    failed = Column('failed', Integer(), nullable=False)
    jumped = Column('jumped', Integer(), nullable=False)

'''
class User(Base):
    """
    用户表
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False, unique=True)
    password = Column(String(32), nullable=False)
    email = Column(String(32), nullable=False, unique=True)

    def __repr__(self):
        return "<%s users.username: %s>" % (self.id, self.username)
'''

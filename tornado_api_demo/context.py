# coding: utf8 
from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from tornado_api_demo.base import BaseObject, BaseError 
from tornado_api_demo.model.factory import Factory
from tornado_api_demo.pyredis import PyRedis


class Context(BaseObject):
    def __init__(self):
        BaseObject.__init__(self)
        self.factory = Factory()


    def init(self, config):
        self.cfg = ConfigParser()
        self.cfg.read(config)
        self.Sessions = {}
        for conn in self.cfg.options('mysql'):
            engine = create_engine(
                    self.cfg.get('mysql', conn), 
                    pool_size=100, pool_recycle=3600)
            self.Sessions[conn] = scoped_session(sessionmaker(bind=engine))
        self.cache = PyRedis(
                host=self.cfg.get('redis', 'host'), 
                pswd=self.cfg.get('redis', 'pswd'), 
                db=self.cfg.getint('redis', 'db'))
        self.factory.init()


    def mksession(self, conn):
        if conn not in self.Sessions:
            raise BaseError('数据库不存在')
        return self.Sessions[conn]()


g_ctx = Context()


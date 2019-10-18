# coding: utf8 
import time
from functools import wraps
from redis import StrictRedis


class PyRedis(object):
    def __init__(self, host, port=6379, pswd='', db=1, version='', 
            retry_interval=60):
        self.version = version
        self.redis = StrictRedis(host=host, port=port, password=pswd, db=db)
        self.retry_interval = retry_interval
        self.last_try = None
        self.status = None
        self.try_connect()

    
    def mkkey(self, key):
        return '{}{}'.format(self.version, key)


    def try_connect(self):
        try:
            self.last_try = time.time()
            self.redis.ping()
            self.status = 'OK'
        except Exception as e:
            self.status = 'GONE'


    def retry(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            if self.status != 'OK':
                if time.time() - self.last_try >= self.retry_interval:
                    self.try_connect()
                return None
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.status = 'GONE'
        return wrapper


    def mkkey(self, key):
        return '{}{}'.format(self.version, key)


    @retry
    def get(self, key, default=None):
        return self.redis.get(self.mkkey(key)) or default


    @retry
    def set(self, key, value, ex=None):
        self.redis.set(self.mkkey(key), value, ex=ex)


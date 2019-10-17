# coding: utf8 
import json
import uuid
import logging
from functools import wraps
from time import mktime, monotonic as now


class BaseError(Exception):
    def __init__(self, error):
        Exception.__init__(self)
        self.error = error


class BaseObject(object):
    def __init__(self, log_name='', log_level=logging.DEBUG):
        self.log = logging.getLogger(log_name or self.__class__.__name__)
        self.log.setLevel(log_level)
        self.log.propagate = False
        if not self.log.handlers:
            fmt = ('[%(name)-24s %(threadName)-14s %(levelname)-8s '
                    '%(asctime)s] %(message)s')
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(fmt))
            self.log.addHandler(handler)
        self.initialized = False


def get_logger(name, level=logging.INFO):
    obj = BaseObject(log_name=name, log_level=level)
    return obj.log


def took(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        obj = args[0]
        start = now()
        r = func(*args, **kwargs)
        ms = (now() - start) * 1000
        obj.log.debug('%s took %.2f ms' % (func.__name__, ms)) 
        return r
    return wrapper


def use_cache(cache, prefix, params=[], ex=5):
    def wrapper(func):
        @wraps(func)
        def inner_wrapper(self, req):
            k = prefix + '.' + '#'.join([req.params.get(p, '') 
                    for p in params])
            req.log.info('search cache for {}'.format(k))
            v = cache.get(k)
            if v is not None:
                try:
                    req.log.info('hit cache')
                    return json.loads(v)
                except Exception as e:
                    req.log.error('invalid cache value')
                    cache.delete(k)
            r = func(self, req)
            cache.set(k, json.dumps(r, ensure_ascii=False), ex=ex)
            return r
        return inner_wrapper
    return wrapper


def del_cache(cache, prefix, params=[]):
    def wrapper(func):
        @wraps(func)
        def inner_wrapper(self, req):
            k = prefix + '.'.join([req.params.get(p, '') for p in params])
            cache.delete(k)
            return func(self, req)
        return inner_wrapper
    return wrapper


def get_uuid():
    return str(uuid.uuid4()).replace('-', '')


# coding: utf8 
import json
import uuid
import logging
from functools import wraps
from time import mktime, monotonic as now


def get_logger(name, level=logging.INFO):
    log = logging.getLogger(name)
    log.setLevel(level)
    log.propagate = False
    if not log.handlers:
        fmt = ('[%(name)-24s %(threadName)-14s %(levelname)-8s '
                '%(asctime)s] %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(fmt))
        log.addHandler(handler)
    return log


def took(func):
    @wraps(func)
    def wrapper(obj, *args, **kwargs):
        start = now()
        r = func(obj, *args, **kwargs)
        ms = (now() - start) * 1000
        obj.log.info('%s took %.2f ms' % (func.__name__, ms)) 
        return r
    return wrapper


def use_cache(cache, prefix, params=[], ex=5):
    def wrapper(func):
        @wraps(func)
        def inner_wrapper(obj, req):
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
            r = func(obj, req)
            cache.set(k, json.dumps(r, ensure_ascii=False), ex=ex)
            return r
        return inner_wrapper
    return wrapper


def del_cache(cache, prefix, params=[]):
    def wrapper(func):
        @wraps(func)
        def inner_wrapper(obj, req):
            k = prefix + '.'.join([req.params.get(p, '') for p in params])
            cache.delete(k)
            return func(obj, req)
        return inner_wrapper
    return wrapper


def get_uuid():
    return str(uuid.uuid4()).replace('-', '')


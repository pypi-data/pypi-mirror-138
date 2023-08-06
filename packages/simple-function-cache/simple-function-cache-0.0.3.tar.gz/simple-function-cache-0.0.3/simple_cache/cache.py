#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/2/8 3:17 下午
# @File    : cache.py
# @author  : Akaya
# @Software: PyCharm
# cache  :  cache logic
import pickle
import logging
import json.encoder
import redis
from enum import Enum
from functools import wraps

logger = logging.getLogger(__name__)


class CallWithCacheException(Exception):
    def __init__(self, message, status):
        super().__init__(message, status)
        self.message = "ProcessWithCacheException " + message
        self.status = status


class CacheMode(Enum):
    cache = "cache"
    no_cache = "no_cache"
    refresh = "fresh"


def default_cache_condition(model_result, *args, **kwargs):
    return True


class FuncCache(object):
    # cache_client
    _redis_client = None
    # 72 hours ( 3 days )
    _defaultCacheTime = 259200
    _defaultHitKey = "__funcCacheHit"
    _defaultMissKey = "__funcCacheMiss"

    def __init__(self, redis_client: redis.Redis):
        self._redis_client = redis_client

    def __call__(self, **kwargs):
        """
        :param kwargs:
            key_func: func() -> str
            cache_condition_func: func() -> bool
            expire: int ( time in seconds )
        :return:
        """
        cache_mode = kwargs.get('cache_mode', 'cache')
        cache_name = kwargs.get('cache_name', 'default_cache')
        no_cache, refresh = False, False
        if cache_mode == CacheMode.no_cache.name:
            no_cache = True
        if cache_mode == CacheMode.refresh.name:
            refresh = True
        key_func = kwargs.get("key_func")
        cache_condition_func = kwargs.get("cache_condition_func", default_cache_condition)

        if not key_func:
            raise CallWithCacheException("key_func should not empty", "")
        if not callable(key_func):
            raise CallWithCacheException("key_func should be callable", "")
        if cache_condition_func and not callable(cache_condition_func):
            raise CallWithCacheException("cache_condition_func should be callable when it is set", "")

        def inner_function(origin_func):

            @wraps(origin_func)
            def exec_cache(*origin_args, **origin_kwargs):
                namespace = str(origin_kwargs.get("namespace"))
                cache_mode_ = str(origin_kwargs.get("cache_mode_"))
                _no_cache = no_cache
                _refresh = refresh
                if cache_mode_ == CacheMode.cache.name:
                    _no_cache, _refresh = False, False
                elif not _no_cache and cache_mode_ == CacheMode.no_cache.name:
                    _no_cache = True
                elif not _refresh and cache_mode_ == CacheMode.refresh.name:
                    _refresh = True

                # no cache, just dry run func
                if _no_cache:
                    logger.info("cache disable - use no cache")
                    return origin_func(*origin_args, **origin_kwargs)
                key_prefix = cache_name + '_'
                cache_key = key_func(*origin_args, **origin_kwargs)
                if type(cache_key) != str:
                    raise CallWithCacheException("key_func should return a str , but got :" + str(type(cache_key)), status='Failed')
                cache_key = key_prefix + cache_key
                # refresh cache , delete old one and set new
                raw_expire = kwargs.get("expire")
                if type(raw_expire) == int:
                    expire = raw_expire
                else:
                    expire = self._defaultCacheTime
                if _refresh:
                    logger.info("remove by refresh : {}".format(cache_key))
                    self._redis_client.delete(cache_key)
                    try:
                        raw_data = origin_func(*origin_args, **origin_kwargs)
                    except Exception as e:
                        logger.error(e)
                        return
                    if cache_condition_func(raw_data, *origin_args, **origin_kwargs):
                        self._redis_client.set(cache_key, pickle.dumps(raw_data), ex=expire)
                    else:
                        logger.info("cache condition is False, refresh failed.")
                    return raw_data
                # normal process get first
                raw_cached_r = self._redis_client.get(cache_key)
                if raw_cached_r:
                    logger.info("get cache hit : {}".format(cache_key))
                    self._redis_client.incr(self._defaultHitKey + "_" + namespace + "_" + cache_name, 1)
                    cached_r = pickle.loads(raw_cached_r)
                    logger.info("from cache : {}".format(cached_r))
                    return cached_r
                origin_data = origin_func(*origin_args, **origin_kwargs)
                if cache_condition_func(origin_data, *origin_args, **origin_kwargs):
                    self._redis_client.set(cache_key, pickle.dumps(origin_data), ex=expire)
                    self._redis_client.incr(self._defaultMissKey + "_" + namespace + "_" + cache_name, 1)
                    logger.info("cache key:  {} - cache_key_func : {}".format(cache_key, key_func))
                else:
                    logger.info("cache condition is False, cache failed.")
                return origin_data

            return exec_cache

        return inner_function

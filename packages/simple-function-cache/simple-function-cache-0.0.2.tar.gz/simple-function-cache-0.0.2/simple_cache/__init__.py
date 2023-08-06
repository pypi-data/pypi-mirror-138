#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/2/8 3:12 下午
# @File    : __init__.py
# @author  : Akaya
# @Software: PyCharm
# __init__.py  :  
from cache_redis.cache import FuncCache, default_cache_condition, CacheMode
from cache_redis.single_redis import RedisSingleton


def build_cache(db, config_json=None):
    model_cache = FuncCache(RedisSingleton.get_instance(db, config_json))
    return model_cache

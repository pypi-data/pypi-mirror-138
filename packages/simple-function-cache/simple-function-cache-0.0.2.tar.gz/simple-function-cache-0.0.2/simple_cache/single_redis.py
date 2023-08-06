#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/2/8 3:13 下午
# @File    : single_redis.py
# @author  : Akaya
# @Software: PyCharm
# single_redis  : model base redis single connector
import logging
import redis
from gevent.lock import Semaphore

logger = logging.getLogger(__name__)


class RedisSingleton:
    lock = Semaphore()
    __instance = None

    def __init__(self):
        logger.info("init RedisSingleton function.")

    @classmethod
    def get_instance(cls, db, config_json=None) -> redis.Redis:
        """
        缓存初始化方法
        :return: redis.Redis
        """
        if not cls.__instance:
            with cls.lock:
                if cls.__instance:
                    return cls.__instance
                logger.info("Init RedisSingleton...")
                host, password, port = config_json['host'], config_json['password'], config_json['port']

                RedisSingleton.__instance = redis.Redis(host=host, password=password, port=port, db=db)
        else:
            logger.info(f"RedisSingleton has been initialized, all param will be ignored, db={db}")
        return RedisSingleton.__instance

    @classmethod
    def clean_instance(cls):
        RedisSingleton.__instance = None

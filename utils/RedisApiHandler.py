# -*- coding: utf-8 -*-

import redis
import logging
from utils import config

__all__ = ['RedisApi']


class RedisApi(object):

    _client = None

    @classmethod
    def connect(cls):
        if cls._client is None:
            cls._client = redis.Redis(
                host=config('REDIS_HOST'),
                db=config('REDIS_DB'),
                port=config('REDIS_PORT'),
                password=config('REDIS_PASSWORD'),
                socket_timeout=0.2,
                socket_connect_timeout=0.2

            )

    @classmethod
    def check_connect(cls):
        try:
            if not cls._client.ping():
                raise ValueError("ping Error")
        except Exception as e:
            logging.error("redis connect Error. retry it. E:{}".format(e))
            cls._client = None
            cls.connect()

    @staticmethod
    def gen_key(source, table ,source_id, _type="fm"):
        return "{}|{}|{}|{}".format(_type, table, source, source_id)

    @classmethod
    def set_cache(cls, cache_key, cache_value):
        try:
            cls.check_connect()
            v = cls._client.set(cache_key, cache_value)
            logging.info("set redis cache success. key:{}, value:{}".format(cache_key, cache_value))
            return v
        except Exception as e:
            logging.error("set redis cache failed. key:{}. e:{}".format(cache_key, e))

    @classmethod
    def get_cache(cls, cache_key):
        cls.check_connect()
        return cls._client.get(cache_key)


# redis_cli = RedisQueueApi()
if __name__ == "__main__":
    from decouple import config
    print (config('SECRET_KEY'))

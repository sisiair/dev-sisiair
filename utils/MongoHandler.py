from utils import config
from pymongo import MongoClient

class MongoHandler(object):
    _client = None
    _db = None

    def _open_client(self):
        self._client = MongoClient(host=config("MONGO_HOST"), port=config("MONGO_PORT", cast=int))
        self._db = self._client[config("MONGO_DATABASE")]

    @property
    def db(self):
        if MongoHandler._db is None:
            self._open_client()
        return self._db

    @property
    def client(self):
        if MongoHandler._client is None:
            self._open_client()
        return self._client

    @staticmethod
    def open():
        return MongoHandler()


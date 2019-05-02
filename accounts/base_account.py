import sys

sys.path.append("..")
from abc import abstractmethod
from utils.MongoHandler import MongoHandler

class BaseAccount(object):
    _mongo = MongoHandler.open()
    _mongo_db = _mongo.db
    _mongo_col = _mongo_db["account"]

    def __init__(self, name, _id = None):
        self.name = name
        self._id = _id
        self.type = None

    @abstractmethod
    def _format(self):
        """
        :return:
        """
        pass

    @abstractmethod
    def _load(self, **kwargs):
        pass

    def save(self):
        """
        将账户存入数据库
        :return:
        """
        data = {"name": self.name, "type": self.type}
        account_info = self._format()
        data.update(account_info)
        is_exist = self._mongo_col.find_one({"name": self.name, "type": self.type})
        if is_exist:
            data = {"$set": data}
            self._mongo_col.update_one({"_id": is_exist["_id"]}, data)
        else:
            self._mongo_col.insert(data)







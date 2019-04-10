import sys

sys.path.append("..")
from utils.AESHandler import AESHandler
from accounts.base_account import BaseAccount

class HuobiAccount(BaseAccount):

    def __init__(self, assces_key, screate_key, **kwargs):
        super().__init__(**kwargs)
        self.type = "huobi"
        self._load(assces_key, screate_key)

    def _load(self, assces_key, screate_key, **kwargs):
        self.assces_key = assces_key
        self.screate_key = screate_key

    def _format(self):
        assces_key, screate_key = AESHandler.encrypt(self.assces_key), AESHandler.encrypt(self.screate_key)
        return {"assces_key": assces_key, "screate_key": screate_key, "type": self.type}

    @staticmethod
    def load_account(name):
        """
        从mongo加载账户
        :param name:
        :return:
        """
        data = BaseAccount._mongo_col.find_one({"name": name, "type": "huobi"})
        if data is None: raise ValueError("账户不存在")
        _id = data.get("_id")
        assces_key, screate_key = data.get("assces_key"), data.get("screate_key")
        assces_key, screate_key = AESHandler.decrypt(assces_key), AESHandler.decrypt(screate_key)
        return HuobiAccount(assces_key.strip(), screate_key, name=name, _id=_id)

if __name__ == "__main__":
    # huobi = HuobiAccount(assces_key, screatekey, name="huobi1")
    # huobi.save()
    huobi = HuobiAccount.load_account("huobi1")
    pass
import sys

sys.path.append("..")
from utils.AESHandler import AESHandler
from accounts.base_account import BaseAccount
from exchanges.TerraChain import TerraChain

class TerraAccount(BaseAccount):

    def __init__(self, address, user_key, **kwargs):
        """

        :param address:
        :param user_key:
        :param kwargs: {"name": str, "_id": str}
        """
        super().__init__(**kwargs)
        self.nonce = None
        self.type = "terra"
        self._load(address, user_key)
        self.__fresh_nonce()

    def __fresh_nonce(self):
        self.nonce = TerraChain.get_address_nonce(self.address)

    def _load(self, address, user_key):
        self.address = address
        self.user_key = user_key

    def _format(self):
        aes_address, aes_key = AESHandler.encrypt(self.address), AESHandler.encrypt(self.user_key)
        return {"address": aes_address, "key": aes_key, "type": self.type}

    @staticmethod
    def load_account(name):
        """
        从mongo加载账户
        :param name:
        :return:
        """
        data = BaseAccount._mongo_col.find_one({"name": name, "type": "terra"})
        if data is None: raise ValueError("账户不存在")
        _id = data.get("_id")
        aes_address, aes_key = data.get("address"), data.get("key")
        address, key = AESHandler.decrypt(aes_address), AESHandler.decrypt(aes_key)
        return TerraAccount(address.strip(), key, name=name, _id=_id)


if __name__ == "__main__":

    # account = CornAccount("test1", "address", "private key")
    # account.save()

    account = TerraAccount.load_account("user1")
    account.save()
    #print ("_id:{}\naddress:{}\nkey:{}".format(account.db_id, account.address, account.user_key))

import copy
import random
import sys

sys.path.append("..")
from utils.AESHandler import AESHandler
from accounts.base_account import BaseAccount
from exchanges.TerraChain import TerraChain


class NoAccount(BaseException):
    pass


class TerraAccount(BaseAccount):
    noncce_cache = {}  # {"user1": 1}

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
        self.clc_balance, self.eth_balance = None, None
        self.fresh_nonce()
        self.save()

    def fresh_nonce(self):
        if self.nonce is None:
            self.nonce = TerraChain.get_address_nonce(self.address)
        if self.address in TerraAccount.noncce_cache:
            max_value = max(self.nonce, TerraAccount.noncce_cache.get(self.address))
            self.nonce, TerraAccount.noncce_cache[self.address] = max_value, max_value
        else:
            TerraAccount.noncce_cache[self.address] = self.nonce

    def fresh_balance(self):
        self.eth_balance = float(TerraChain.get_eth_balance(self.address))
        self.clc_balance = float(TerraChain.get_clc_balance(self.address))

    def _load(self, address, user_key):
        self.address = address
        self.user_key = user_key

    def _format(self):
        aes_address, aes_key = AESHandler.encrypt(self.address), AESHandler.encrypt(self.user_key)
        return {"address": aes_address,
                "key": aes_key,
                "type": self.type,
                "clc_balance": self.clc_balance,
                "eth_balance": self.eth_balance}

    def save(self):
        self.fresh_balance()
        super(TerraAccount, self).save()

    @staticmethod
    def load_account(query):
        datas = BaseAccount._mongo_col.find(query)
        data = random.choice(list(datas))
        if data is None: raise NoAccount()
        _id = data.get("_id")
        aes_address, aes_key, name = data.get("address"), data.get("key"), data.get("name")
        address, key = AESHandler.decrypt(aes_address), AESHandler.decrypt(aes_key)
        return TerraAccount(address.strip(), key, name=name, _id=_id)

    @staticmethod
    def load_account_with_name(name):
        """
        从mongo加载账户
        :param name:
        :return:
        """
        return TerraAccount.load_account({"name": name, "type": "terra"})


if __name__ == "__main__":
    # account = CornAccount("test1", "", "")
    # account.save()

    account = TerraAccount.load_account_with_name("user1")
    account.save()
    # print ("_id:{}\naddress:{}\nkey:{}".format(account.db_id, account.address, account.user_key))

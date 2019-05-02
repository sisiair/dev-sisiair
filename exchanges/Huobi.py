import base64
import datetime
import hashlib
import hmac
from utils import config
from utils.webHandler import WebHandler
from urllib.parse import urlparse, urlencode
from exchanges.Base import BaseExchange
from huobi import RequestClient
from huobi.model import *


class Huobi(BaseExchange):

    def __init__(self):
        self.request_client = RequestClient(api_key=config('API_KEY'),
                                       secret_key=config('SECRET_KEY'))

    def buy_token(self, trading_pair, trade_amount, trade_price):
        return self.request_client.create_order(trading_pair, AccountType.SPOT, OrderType.BUY_LIMIT, trade_amount, trade_price)

    def sell_token(self, trading_pair, trade_amount, trade_price):
        return self.request_client.create_order(trading_pair, AccountType.SPOT, OrderType.SELL_LIMIT, trade_amount, trade_price)

    def get_balance(self):
        """
        获取金币
        :return:
        """
        pass

    def get_balance_tokens(self):
        pass

    @classmethod
    def get_exchange(cls):
        return cls()

    @staticmethod
    def get_order_book(limit=1):
        pass


if __name__ == "__main__":
    hb = Huobi()
    ff=hb.request_client.get_exchange_timestamp()
    by = hb.sell_token('ethbtc',0.001, 1.0)
    o=0


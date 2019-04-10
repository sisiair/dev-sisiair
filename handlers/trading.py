import sys
import logging
sys.path.append("..")

from accounts.terra_account import TerraAccount
from accounts.huobi_account import HuobiAccount
from exchanges.TerraChain import TerraChain
from exchanges.Huobi import Huobi
logger = logging.getLogger()

class Trading():
    """
    交易类
    """

    def __init__(self, account_name, exchange_type):
        # 打开协议， 加载帐号
        self.exchange_type = exchange_type
        if exchange_type == "terra":
            self.exchange = TerraChain.get_exchange()
            self.account = TerraAccount.load_account(account_name)
        elif exchange_type == "huobi":
            self.exchange = Huobi.get_exchange()
            self.account = HuobiAccount.load_account(account_name)


    def sell_token(self, price, amount):
        """
        卖出虚拟币
        :param price: 价格
        :param amount: 数量
        :return:
        """
        trade_result = self.exchange.sell_token(self.account, amount, price)
        # self.account.nonce += 1
        logger.info("finish sell token trade, account: {}, price: {}, amount: {}"
                    .format(self.account.name, price, amount))
        return trade_result

    def buy_token(self, price, amount):
        """
        买进虚拟币
        :param price: 价格
        :param amount: 数量
        :return:
        """
        trade_result =  self.exchange.buy_token(self.account, amount, price)
        logger.info("finish buy token trade, account: {}, price: {}, amount: {}"
                    .format(self.account.name, price, amount))
        return trade_result

    def batch_trade(self, trades):
        """
        批量交易
        :param trades: ["sell or buy", 数目, 价格]
        :return:
        """
        for trade, amount, price in trades:
            if trade not in ["sell_token", "buy_token"]: continue
            try:
                m = self.__getattribute__(trade)
                m(price, amount)
                logger.info("finish trade type: {}, amount: {}, price: {}".format(trade, amount, price))
            except Exception as e:
                logger.error("failed trade type: {}, amount: {}, price: {}\n{}".format(trade, amount, price, e))


if __name__ == "__main__":
    pass

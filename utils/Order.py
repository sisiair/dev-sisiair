from exchanges.TerraChain import TerraChain
from exchanges.Huobi import Huobi

class Order(object):

    def __init__(self,exchange_type):
        self.trade_id = None
        self.amount = None
        self.total_amount = None
        self.price = None
        self.trade_time = None
        self.direction = None
        self.trading_pair = None
        self.filled = None
        self.unfilled = None
        if exchange_type == "terra":
            self.exchange = TerraChain.get_exchange()
        elif exchange_type == "huobi":
            self.exchange = Huobi.get_exchange()

    def save(self):
        pass

    def get_open_orders(self):
        self.exchange.get_order_book()

    def get_order_history(self):
        pass

    def get_partital_histroy(self):
        pass

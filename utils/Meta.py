class Meta(object):

    def __init__(self, trade_id, amount,*args, **kwargs):
        self.trade_id = trade_id
        self.amount = amount

        self.price = None
        self.buy_account = None
        self.sell_account = None
        self.trade_buy_status = None
        self.trade_sell_status = None
        self.trade_buy_order_id = None
        self.trade_sell_order_id = None


class Track(object):

    def __init__(self, *args, **kwargs):
        self.start = None
        self.high = None
        self.low = None

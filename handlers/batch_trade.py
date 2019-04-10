import sys
sys.path.append("..")
from handlers.trading import Trading
from utils.random_factory import RandomFactory as rf

class BatchTrade:

    def __init__(self, account_name, chain_type):
        self._trade = Trading(account_name, chain_type)

    def trade(self, batch_amount, batch_type, price_func, price_para, amount_func, amount_para):
        """
        调用买卖函数
        :param batch_amount: 交易数目
        :param batch_type: buy/sell/random
        :param
        :param amount: 买卖数目
        :param func: 生成函数
            normal_distribution **kwargs {mu, sigma}
        :param kwargs: 生成参数，
        :return:
        """
        func_map = {
            "normal_distribution": rf.normal_distribution_trade,
            "uniform_distribution": rf.random_uniform,
            "trunc_normal": rf.trunc_normal
        }
        my_price_func = func_map.get(price_func)
        my_amount_func = func_map.get(amount_func)
        price_para["num"] = batch_amount
        amount_para["num"] = batch_amount
        price = my_price_func(**price_para)
        amount = my_amount_func(**amount_para)
        for n in range(0, batch_amount):
            batch = ("{}_token".format(batch_type), abs(int(amount[n])), abs(round(price[n], 7)))
            self._trade.batch_trade([batch])


if __name__ == "__main__":
    pass
    # i = int(random.normalvariate(5, 1) * 2)
    # pass
    # batch_trade = BatchTrade("user1")
    # batch_trade.trade(5, "buy", 50, "normal_distribution")
    # print(BatchTrade.random_uniform(2, 10))

#! /Users/orion/anaconda3/envs/exchange/bin/python
import sys

sys.path.append("..")
from handlers.batch_trade import BatchTrade
import argparse


def parse_avg():
    parser = argparse.ArgumentParser(description="调用批量交易程序")
    parser.add_argument('--account', '-u', required=True, type=str)
    parser.add_argument('--batch_type', '-t', choices=['buy', 'sell', 'random'], required=True, type=str)
    parser.add_argument('--batch_amount', '-a', type=int, default=5)
    # 生成数量函数
    parser.add_argument('--amount_func', choices=["normal_distribution", "uniform_distribution"], type=str,
                        default="normal_distribution")
    parser.add_argument('--amount_para', type=str, default={})
    # 生成价格函数
    parser.add_argument('--price_func', choices=["normal_distribution", "uniform_distribution","trunc_normal"], type=str,
                        default="normal_distribution")
    parser.add_argument('--price_para', type=str, default={})
    parser.add_argument('--chain', type=str, choices=["terra", "huobi"])

    return parser.parse_args()


def trade(bus):
    account, batch_type, batch_amount, amount_func, amount_para, price_func, price_para, chain  = \
        bus.account, bus.batch_type, bus.batch_amount, \
        bus.amount_func, eval(bus.amount_para), bus.price_func, eval(bus.price_para), bus.chain
    batch_trade = BatchTrade(account_name=account, chain_type=chain)
    batch_trade.trade(batch_amount, batch_type, price_func, price_para, amount_func, amount_para)


if __name__ == "__main__":
    args = parse_avg()
    trade(args)

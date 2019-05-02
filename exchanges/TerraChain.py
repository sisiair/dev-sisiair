import os
import json
import logging
from web3 import Web3
from utils import config
from bson import ObjectId
from datetime import datetime
from utils import BASE_FILE_DIR
from exchanges.Base import BaseExchange
from exchanges.apis import Terrachain_api

from shell import loop

logger = logging.getLogger()



class TerraChain(BaseExchange):
    web3Instance = None
    erc827 = None
    my_erc827 = None
    exchange = None

    def __init__(self, Exchangeabi, ERC827abi, MyERC827abi, trade_token_add, rpc_url):
        self.trade_token_add = trade_token_add
        if TerraChain.web3Instance is None: TerraChain.web3Instance = Web3(
            Web3.HTTPProvider(rpc_url, request_kwargs={'timeout': 240}))
        if TerraChain.erc827 is None: TerraChain.erc827 = self.web3Instance.eth.contract(abi=ERC827abi, address=config(
            'ETH_TOKEN_ADDRESS'))
        if TerraChain.my_erc827 is None: TerraChain.my_erc827 = self.web3Instance.eth.contract(abi=MyERC827abi,
                                                                                               address=config(
                                                                                                   'ETH_TOKEN_ADDRESS'))
        if TerraChain.exchange is None: TerraChain.exchange = self.web3Instance.eth.contract(abi=Exchangeabi,
                                                                                             address=config(
                                                                                                 'EXCHANGE_ADDRESS'))

    def gen_trade_id(self):
        return ObjectId.from_datetime(datetime.now())

    def is_trade_success(self, tx_hash):
        status = self.web3Instance.eth.getTransactionReceipt(tx_hash)
        if status is None:
            logger.debug("tx_hash {}".format( tx_hash))
            return self.is_trade_success(tx_hash)
        if status["status"] is None:
            return self.is_trade_success(tx_hash)
        return False if status["status"] == 0 else True

    async def buy_token(self, account, tradeTokenAmount, tradePrice):
        #account.fresh_nonce()
        tx_hash = Terrachain_api._buy_token(self.web3Instance, self.exchange, self.erc827,
                                                      self.trade_token_add, account.address, account.user_key,
                                                      account.nonce, tradeTokenAmount, tradePrice)
        r = self.is_trade_success( tx_hash)
        account.nonce += 1
        account.save()
        return r

    async def sell_token(self, account, tradeTokenAmount, tradePrice):
        #account.fresh_nonce()
        tx_hash = Terrachain_api._sell_token(self.web3Instance, self.exchange,
                                                      self.trade_token_add, account.address, account.user_key, account.nonce, tradeTokenAmount,
                                             tradePrice)
        r = self.is_trade_success( tx_hash)
        account.nonce += 1
        account.save()
        return r



    @staticmethod
    def get_order_book(limit=1):
        terra_handler = TerraChain.get_exchange()
        asks = terra_handler.exchange.functions.getAsks(limit, terra_handler.trade_token_add,
                                                        config('ETH_TOKEN_ADDRESS')).call()
        bids = terra_handler.exchange.functions.getBids(limit, terra_handler.trade_token_add,
                                                        config('ETH_TOKEN_ADDRESS')).call()
        return bids, asks

    @staticmethod
    def get_last_ask(limit=1):
        terra_handler = TerraChain.get_exchange()
        asks = terra_handler.exchange.functions.getAsks(limit, terra_handler.trade_token_add,
                                                        config('ETH_TOKEN_ADDRESS')).call()
        return asks

    @staticmethod
    def cancel_open_order(account, order_id):
        terra_handler = TerraChain.get_exchange()
        #account.fresh_nonce()
        tx_hash= Terrachain_api.cancel_order(terra_handler.web3Instance, terra_handler.exchange,order_id, account.user_key, account.nonce)
        r = terra_handler.is_trade_success(tx_hash)
        account.nonce += 1
        account.save()
        return r

    @classmethod
    def get_exchange(cls):
        clc_address, rpc_url = config("CLC_ADDRESS"), config("RPC_URL")
        exchange, ERC827abi, MyERC827Token = config("Exchange_FILE"), \
                                             config("ERC827abi_FILE"), \
                                             config("MyERC827Token_FILE")
        with open(os.path.join(BASE_FILE_DIR, exchange), "r") as f: Exchangeabi = json.load(f)
        with open(os.path.join(BASE_FILE_DIR, ERC827abi), "r") as f: ERC827abi = json.load(f)
        with open(os.path.join(BASE_FILE_DIR, MyERC827Token), "r") as f: MyERC827abi = json.load(f)
        return cls(Exchangeabi, ERC827abi, MyERC827abi, clc_address, rpc_url)

    @staticmethod
    def get_address_nonce(address):
        terra_chain = TerraChain.get_exchange()
        return Terrachain_api.get_user_nonce(terra_chain.web3Instance, address)

    @staticmethod
    def get_clc_balance(user_address):
        terra_chain = TerraChain.get_exchange()
        return terra_chain.web3Instance.eth.getBalance(user_address)

    @staticmethod
    def get_eth_balance(user_address):
        terra_chain = TerraChain.get_exchange()
        return terra_chain.my_erc827.functions.balanceOf(user_address).call()

    def get_balance_tokens(self, user_address, address):
        MyERC827Token = config("MyERC827Token_FILE")
        with open(os.path.join(BASE_FILE_DIR, MyERC827Token), "r") as f: MyERC827Tokenabi = json.load(f)
        myerc827token = self.web3Instance.eth.contract(abi=MyERC827Tokenabi, address=address)
        return myerc827token.functions.balanceOf(user_address).call()

    @staticmethod
    def getOrder(order_id):
        terra_handler = TerraChain.get_exchange()
        return terra_handler.exchange.functions.getOrder(order_id).call()

if __name__ == "__main__":
    '''
    import sys

    sys.path.append("..")
    ex = TerrachainHandler.get_exchange()
    # aa = ex.web3Instance.eth.defaultBlock
    # pass
    a = ex.get_order_book(1)
    pass
    '''
    #ex = TerraChain.get_exchange()
    #ss = ex.get_balance_tokens('0x8cBC24A319810385117E10e2F2D7E1389C15665b',
    #                           "0x01E85faB199F183FA4821ebBB184a4Dfc5dd459a")


    from utils import config

    limit = 10

    timerage = [0, 999999999999999]
    tradetoken = '0x0000000000000000000000000000000000000000'
    basetoken = config('ETH_TOKEN_ADDRESS')
    ddd=Terrachain_api.get_trade_history(limit, timerage, tradetoken, basetoken)
    print(ddd[1])
    f = 000
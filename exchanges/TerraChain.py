import os
import json
import logging
from web3 import Web3
from utils import config
from bson import ObjectId
from datetime import datetime
from utils import BASE_FILE_DIR
from exchanges.Base import BaseExchange
logger = logging.getLogger()

class TerraChain(BaseExchange):

    def __init__(self, Exchangeabi, ERC827abi, trade_token_add, rpc_url):
        self.trade_token_add = trade_token_add
        self.web3Instance = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={'timeout': 240}))
        self.erc827 = self.web3Instance.eth.contract(abi=ERC827abi, address=config('ETH_TOKEN_ADDRESS'))
        self.exchange = self.web3Instance.eth.contract(abi=Exchangeabi, address=config('EXCHANGE_ADDRESS'))

    def gen_trade_id(self):
        return ObjectId.from_datetime(datetime.now())

    def is_trade_success(self, trade_id, tx_hash):
        status = self.web3Instance.eth.getTransactionReceipt(tx_hash)
        if status is not None:
            logger.debug("{}, tx_hash {}, trade status {}".format(trade_id, tx_hash, status["status"]))
        if status is not None and status["status"] == 1:
            return True
        return False

    def _buy_token(self, user_address, user_key, nonce, tradeTokenAmount, tradePrice):
        trade_id = self.gen_trade_id()
        logger.debug("{}, start buy_trade user_address: {}, tradeTokenAmount: {}, "
                    "tradePrice: {}, nonce: {}".format(trade_id, user_address, tradeTokenAmount,
                                                       tradePrice, nonce))
        baseTokenAmount = tradeTokenAmount * tradePrice
        buyData = self.exchange.functions.buy(config('ETH_TOKEN_ADDRESS'), self.trade_token_add,
                                              user_address, self.web3Instance.toWei(str(tradeTokenAmount), 'ether'),
                                              self.web3Instance.toWei(str(tradePrice), 'ether')).buildTransaction(
            {'gas': 500000000, 'gasPrice': self.web3Instance.toWei('6', 'gwei'), 'nonce': nonce, })

        txData = self.erc827.functions.approveAndCall(config('EXCHANGE_ADDRESS'),
                                                      self.web3Instance.toWei(baseTokenAmount, 'ether'),
                                                      buyData['data']).buildTransaction(
            {'gas': 500000000, 'gasPrice': self.web3Instance.toWei('6', 'gwei'), 'nonce': nonce, })
        signed_txn = self.web3Instance.eth.account.signTransaction(txData, private_key=user_key)
        tx_hash = self.web3Instance.eth.sendRawTransaction(signed_txn.rawTransaction)
        logger.debug("{}, trade format data, send RawTransaction success".format(trade_id))
        return self.is_trade_success(trade_id, tx_hash)

    def _sell_token(self, user_address, user_key, nonce, tradeTokenAmount, tradePrice):
        trade_id = self.gen_trade_id()
        logger.debug("{}, start buy_trade user_address: {}, tradeTokenAmount: {}, "
                     "tradePrice: {}, nonce: {}".format(trade_id, user_address, tradeTokenAmount,
                                                        tradePrice, nonce))
        sellData = self.exchange.functions.sell(config('ETH_TOKEN_ADDRESS'), self.trade_token_add,
                                                user_address,
                                                self.web3Instance.toWei(str(tradeTokenAmount), 'ether'),
                                                self.web3Instance.toWei(str(tradePrice), 'ether')).buildTransaction(
            {'gas': 50000000, 'gasPrice': self.web3Instance.toWei('6', 'gwei'), 'nonce': nonce,
             'value': self.web3Instance.toWei(str(tradeTokenAmount), 'ether')})

        signed_txn = self.web3Instance.eth.account.signTransaction(sellData, private_key=user_key)
        tx_hash = self.web3Instance.eth.sendRawTransaction(signed_txn.rawTransaction)
        logger.debug("{}, trade format data, send RawTransaction success".format(trade_id))
        return self.is_trade_success(trade_id, tx_hash)

    def buy_token(self, account, tradeTokenAmount, tradePrice):
        self._buy_token(account.address, account.user_key, account.nonce, tradeTokenAmount, tradePrice)
        account.nonce += 1

    def sell_token(self, account, tradeTokenAmount, tradePrice):
        self._sell_token(account.address, account.user_key, account.nonce, tradeTokenAmount, tradePrice)
        account.nonce += 1

    def get_open_orders(self, user_address):
        open_orders = self.exchange.functions.getUserOpenOrders(user_address, self.trade_token_add,
                                                                config('ETH_TOKEN_ADDRESS')).call()
        return open_orders

    def cancel_order(self, order_id, user_key, nonce):
        cancelData = self.exchange.functions.cancelOrder(order_id).buildTransaction(
            {'gas': 50000000, 'gasPrice': self.web3Instance.toWei('5', 'gwei'), 'nonce': nonce})

        signed_txn = self.web3Instance.eth.account.signTransaction(cancelData,
                                                                   private_key=user_key)
        txhash = self.web3Instance.eth.sendRawTransaction(signed_txn.rawTransaction)
        return txhash.hex()



    def get_user_nonce(self, user_address):
        nonce = self.web3Instance.eth.getTransactionCount(user_address)
        return nonce

    @staticmethod
    def get_order_book(limit=1):
        terra_handler = TerraChain.get_exchange()
        asks = terra_handler.exchange.functions.getAsks(limit, terra_handler.trade_token_add, config('ETH_TOKEN_ADDRESS')).call()
        bids = terra_handler.exchange.functions.getBids(limit, terra_handler.trade_token_add, config('ETH_TOKEN_ADDRESS')).call()
        return  bids[2][0] / 10 ** 18, asks[2][0] / 10 ** 18

    @classmethod
    def get_exchange(cls):
        clc_address, rpc_url = config("CLC_ADDRESS"), config("RPC_URL")
        exchange, ERC827abi = config("Exchange_FILE"), config("ERC827abi_FILE")
        with open(os.path.join(BASE_FILE_DIR, exchange), "r") as f: Exchangeabi = json.load(f)
        with open(os.path.join(BASE_FILE_DIR, ERC827abi), "r") as f: ERC827abi = json.load(f)
        return cls(Exchangeabi, ERC827abi, clc_address, rpc_url)

    @staticmethod
    def get_address_nonce(address):
        terra_chain = TerraChain.get_exchange()
        return terra_chain.get_user_nonce(address)

    @staticmethod
    def get_balance(user_address):
        terra_chain = TerraChain.get_exchange()
        return terra_chain.web3Instance.eth.getBalance(user_address,
                                                       block_identifier=config('CLC_ADDRESS'))

    def get_balance_tokens(self, user_address, address):
        MyERC827Token = config("MyERC827Token_FILE")
        with open(os.path.join(BASE_FILE_DIR, MyERC827Token), "r") as f: MyERC827Tokenabi = json.load(f)
        myerc827token = self.web3Instance.eth.contract(abi=MyERC827Tokenabi, address=address)
        return myerc827token.functions.balanceOf(user_address).call()



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
    ex = TerraChain.get_exchange()
    ss=ex.get_balance_tokens('0x8cBC24A319810385117E10e2F2D7E1389C15665b',"0x01E85faB199F183FA4821ebBB184a4Dfc5dd459a")

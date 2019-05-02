import logging
from utils import config
from web3.gas_strategies.rpc import rpc_gas_price_strategy


logger = logging.getLogger()


def _buy_token(web3Instance, exchange, erc827, trade_token_add, user_address, user_key, nonce, tradeTokenAmount, tradePrice):
    #gasprice = web3Instance.eth.setGasPriceStrategy(rpc_gas_price_strategy)
    fff=web3Instance.toWei('1', 'gwei')
    gas_ = 2500000

    logger.debug("start buy_trade user_address: {}, tradeTokenAmount: {}, "
                 "tradePrice: {}, nonce: {}".format( user_address, tradeTokenAmount,
                                                    tradePrice, nonce))
    baseTokenAmount = tradeTokenAmount * tradePrice
    buyData = exchange.functions.buy(config('ETH_TOKEN_ADDRESS'), trade_token_add,
                                          user_address, web3Instance.toWei(str(tradeTokenAmount), 'ether'),
                                          web3Instance.toWei(str(tradePrice), 'ether')).buildTransaction(
        {'gas': gas_, 'gasPrice': web3Instance.toWei('1', 'wei'), 'nonce': nonce, })


    '''
    estimatedGasLimit= int(self.erc827.functions.approveAndCall\
        (config('EXCHANGE_ADDRESS'), self.web3Instance.toWei(baseTokenAmount, 'ether'), buyData['data']).\
        estimateGas({'from': user_address})*1.2)
    '''

    txData = erc827.functions.approveAndCall(config('EXCHANGE_ADDRESS'),
                                                  web3Instance.toWei(baseTokenAmount, 'ether'),
                                                  buyData['data']).buildTransaction(
        {'gas': gas_, 'gasPrice': web3Instance.toWei('1', 'gwei'), 'nonce': nonce, })
    signed_txn = web3Instance.eth.account.signTransaction(txData, private_key=user_key)
    tx_hash = web3Instance.eth.sendRawTransaction(signed_txn.rawTransaction)
    logger.debug("trade format data, send RawTransaction success")
    return tx_hash


def _sell_token(web3Instance, exchange,trade_token_add, user_address, user_key, nonce, tradeTokenAmount, tradePrice):
    # web3Instance.eth.setGasPriceStrategy(fast_gas_price_strategy)

    gas_ = 2500000

    logger.debug(" start buy_trade user_address: {}, tradeTokenAmount: {}, "
                 "tradePrice: {}, nonce: {}".format(user_address, tradeTokenAmount,
                                                    tradePrice, nonce))

    sss=web3Instance.toWei(str(tradeTokenAmount), 'ether')


    sellData = exchange.functions.sell(config('ETH_TOKEN_ADDRESS'), trade_token_add,
                                            user_address,
                                            web3Instance.toWei(str(tradeTokenAmount), 'ether'),
                                            web3Instance.toWei(str(tradePrice), 'ether')).buildTransaction(
        {'gas': gas_, 'gasPrice': web3Instance.toWei('1', 'gwei'), 'nonce': nonce,
         'value': web3Instance.toWei(str(tradeTokenAmount), 'ether')})

    # estimatedGasLimit = self.exchange.functions.sell(config('ETH_TOKEN_ADDRESS'), self.trade_token_add,
    #                                                 user_address,
    #                                                 self.web3Instance.toWei(str(tradeTokenAmount), 'ether'),
    #                                                 self.web3Instance.toWei(str(tradePrice), 'ether')).
    # estimateGas({'from': user_address})

    signed_txn = web3Instance.eth.account.signTransaction(sellData, private_key=user_key)
    tx_hash = web3Instance.eth.sendRawTransaction(signed_txn.rawTransaction)
    logger.debug(" trade format data, send RawTransaction success")
    # return self.is_trade_success(trade_id, tx_hash)
    return tx_hash


def get_user_nonce(web3Instance, user_address):
    nonce = web3Instance.eth.getTransactionCount(user_address)
    return nonce


def cancel_order(web3Instance, exchange, order_id, user_key, nonce):
    cancelData = exchange.functions.cancelOrder(order_id).buildTransaction(
        {'gas': 50000000, 'gasPrice': web3Instance.toWei('1', 'gwei'), 'nonce': nonce})

    signed_txn = web3Instance.eth.account.signTransaction(cancelData, private_key=user_key)
    txhash = web3Instance.eth.sendRawTransaction(signed_txn.rawTransaction)
    return txhash.hex()


def get_open_orders( user_address):
    from exchanges.TerraChain import TerraChain
    terra_handler = TerraChain.get_exchange()
    open_orders = terra_handler.exchange.functions.getUserOpenOrders(user_address, terra_handler.trade_token_add,
                                                            config('ETH_TOKEN_ADDRESS')).call()
    return open_orders


def get_trade_history(limit, timerage, tradetoken, basetoken):
    from exchanges.TerraChain import TerraChain
    terra_handler = TerraChain.get_exchange()
    order_history = terra_handler.exchange.functions.getTradeHistory(limit, timerage, tradetoken, basetoken).call()
    return order_history




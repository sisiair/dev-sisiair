import base64
import datetime
import hashlib
import hmac
from utils import config
from utils.webHandler import WebHandler
from urllib.parse import urlparse, urlencode
from exchanges.Base import BaseExchange


class Huobi(BaseExchange):

    def __init__(self):
        self.api_url = config("huobi_api_url")

    def api_key_get(self, access_key, secret_key, request_path, params):
        method = 'GET'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params.update({'AccessKeyId': access_key,
                       'SignatureMethod': 'HmacSHA256',
                       'SignatureVersion': '2',
                       'Timestamp': timestamp})

        host_name = urlparse(self.api_url).hostname
        host_name = host_name.lower()
        params['Signature'] = Huobi.createSign(params, method, host_name, request_path, secret_key)
        url = self.api_url + request_path
        return WebHandler.http_get_request(url, params)

    def api_key_post(self, access_key, secret_key, request_path, params):
        method = 'POST'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params_to_sign = {'AccessKeyId': access_key,
                          'SignatureMethod': 'HmacSHA256',
                          'SignatureVersion': '2',
                          'Timestamp': timestamp}

        host_name = urlparse(self.api_url).hostname
        host_name = host_name.lower()
        params_to_sign['Signature'] = Huobi.createSign(params_to_sign, method, host_name,
                                                       request_path, secret_key)
        url = self.api_url + request_path + '?' + urlencode(params_to_sign)
        return WebHandler.http_post_request(url, params)

    @staticmethod
    def createSign(Params, method, host_url, request_path, secret_key):
        sorted_params = sorted(Params.items(), key=lambda d: d[0], reverse=False)
        encode_params = urlencode(sorted_params)
        payload = [method, host_url, request_path, encode_params]
        payload = '\n'.join(payload)
        payload = payload.encode(encoding='UTF8')
        secret_key = secret_key.encode(encoding='UTF8')
        digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest)
        signature = signature.decode()
        return signature

    # 查询当前委托、历史委托
    def _orders_list(self, access_key, secret_key, symbol, states, types=None,
                     start_date=None, end_date=None, _from=None, direct=None, size=None):
        """

        :param symbol:
        :param states: 可选值 {pre-submitted 准备提交, submitted 已提交, partial-filled 部分成交, partial-canceled 部分成交撤销, filled 完全成交, canceled 已撤销}
        :param types: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
        :param start_date:
        :param end_date:
        :param _from:
        :param direct: 可选值{prev 向前，next 向后}
        :param size:
        :return:
        """
        params = {'symbol': symbol,
                  'states': states}

        if types:
            params['types'] = types
        if start_date:
            params['start-date'] = start_date
        if end_date:
            params['end-date'] = end_date
        if _from:
            params['from'] = _from
        if direct:
            params['direct'] = direct
        if size:
            params['size'] = size
        url = '/v1/order/orders'
        return self.api_key_get(access_key, secret_key, url, params)

    # 下单

    # 创建并执行订单
    def _send_order(self, access_key, secret_key, amount, source, symbol, _type, price=0):
        """
        :param amount:
        :param source: 如果使用借贷资产交易，请在下单接口,请求参数source中填写'margin-api'
        :param symbol:
        :param _type: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
        :param price:
        :return:
        """

        params = {"account-id": access_key,
                  "amount": amount,
                  "symbol": symbol,
                  "type": _type,
                  "source": source}
        if price:
            params["price"] = price

        url = '/v1/order/orders/place'
        return self.api_key_post(access_key, secret_key, params, url)

    def buy_token(self, account, trade_amount, trade_price):
        """
        买进虚拟币
        :return:
        """
        access_key, secret_key = account.assces_key, account.screate_key
        self._send_order(access_key, secret_key, _type="buy-limit",
                         price=trade_price, amount=trade_amount, source="api",
                         symbol="ethbtc")

    def sell_token(self, account, trade_amount, trade_price):
        """
        卖出虚拟币
        :return:
        """
        access_key, secret_key = account.assces_key, account.screate_key
        self._send_order(access_key, secret_key, _type="sell-limit",
                         price=trade_price, amount=trade_amount, source="api",
                         symbol="ethbtc")

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
    def getOrderBook(limit=1):
        pass




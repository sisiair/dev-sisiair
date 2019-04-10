from abc import abstractmethod

class BaseExchange:


    @abstractmethod
    def buy_token(self, **kwargs):
        pass

    @abstractmethod
    def sell_token(self, **kwargs):
        pass

    @abstractmethod
    def get_balance(self, **kwargs):
        pass

    @abstractmethod
    def get_balance_tokens(self, **kwargs):
        pass
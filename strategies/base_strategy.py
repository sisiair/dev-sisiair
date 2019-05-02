from abc import abstractmethod


class BaseStrategy:

    @abstractmethod
    def generate_price(self, **kwargs):
        pass

    @abstractmethod
    def generate_amount(self, **kwargs):
        pass

    @abstractmethod
    def trade(self, **kwargs):
        pass

    abstractmethod
    def choose_accounts(self, **kwargs):
        pass

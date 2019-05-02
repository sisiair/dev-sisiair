import numpy as np
from scipy.stats import truncnorm


class RandomFactory:

    @staticmethod
    def trunc_poisson(lam, size):
        X = np.random.poisson(lam, size=size + 1)
        #S = [np.sum(X[0:i]) for i in range(size)]
        return X[1:]

    @staticmethod
    def normal_distribution_trade(mu, sigma):
        return np.random.normalvariate(mu, sigma)

    @staticmethod
    def random_uniform(start, end, num):
        return np.random.uniform(start, end, size=num)

    @staticmethod
    def trunc_normal(start, end, num):
        return truncnorm.rvs(start, end, size=num)

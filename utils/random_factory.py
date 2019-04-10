import numpy as np
from scipy.stats import truncnorm


class RandomFactory:


    @staticmethod
    def random_uniform(start, end, num):
        return np.random.uniform(start, end, size=num)


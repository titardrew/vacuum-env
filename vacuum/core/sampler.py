import numpy as np

def get_uniform_sampler(dim):

    def sampler():
        i, j = np.random.randint(low=0, high=dim, size=2)
        return i, j

    return sampler

from scipy.stats import binom, randint

class user_flyweight:

    '''Defines user flyweight'''

    @staticmethod
    def set_sign(alg : str) -> None:
        '''Sets signature algorithm'''
        sign_alg = { 
                    "uniform" : user_flyweight.uniform, 
                    "binom" : user_flyweight.binom
        }
        user_flyweight.sign = sign_alg[alg]

    @classmethod
    def fuzzy_distribution(cls, fixed_val, w, n):
        '''Extracts a fuzzy secret key from user fuzzy selected distribution'''
        return cls.sign(fixed_val, w, n)
    
    @staticmethod
    def uniform(m : int, w : int, n : int) -> int:
        '''Samples a value from uniform distribution with given mean'''
        return (m + randint.rvs(-w, w+1)) % n

    @staticmethod
    def binom(m : int, w : int, mod : int) -> int:
        '''Samples a value from binomial distribution with given mean'''
        n = 2*w
        p = 0.5
        return binom.rvs(n, p, loc = m-w) % mod
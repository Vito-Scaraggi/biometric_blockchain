from Crypto.Hash import keccak
from time import perf_counter

class tools:

    '''Defines some useful functions'''

    @classmethod
    def hash(cls, m : str, db : int = 256):
        '''Hashes given message'''
        d = keccak.new(digest_bits=db)
        d.update(str(m).encode('utf8'))
        return d.hexdigest()
    
    @classmethod
    def hashint(cls, m : str, db : int = 256):
        '''Hashes given message and converts it to integer'''
        return int( cls.hash(m, db), 16)
    
    def crono(func):
        '''Implements a decorator for timing functions'''
        def inner(*args, **kwargs):
            start = perf_counter()
            x = func(*args, **kwargs)
            end = perf_counter()
            return (end - start, ) + x
        return inner
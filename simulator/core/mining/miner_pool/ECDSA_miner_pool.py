from fastecdsa.curve import secp256k1
from fastecdsa.point import Point

from core.mining.miner_pool.miner_pool import miner_pool
from core.mining.miner.ECDSA_miner import ECDSA_miner
from core.mining.miner_flyweight import miner_flyweight as mf

class ECDSA_miner_pool(miner_pool):

    '''Defines a pool of ECDSA miners'''

    def __init__(self, settings : dict) -> None:
        
        '''Creates a ECDSA miner pool'''

        super(ECDSA_miner_pool, self).__init__(settings)
        
    def configure_flyweight(self, settings : dict) -> None:
        
        '''
            Configure miner flyweight for ECDSA protocol
        '''

        super(ECDSA_miner_pool, self).configure_flyweight(settings)
        #ecdsa
        mf.n = settings["ECDSA"]["n"]
        mf.q = settings["ECDSA"]["q"]
        mf.Gx = settings["ECDSA"]["Gx"]
        mf.Gy = settings["ECDSA"]["Gy"]
        mf.G = Point( mf.Gx, mf.Gy, curve=secp256k1)
        mf.G_ = mf.G * mf.prng_a

    def get_miner_cls(self):
        '''Returns ECDSA miner class'''
        return ECDSA_miner
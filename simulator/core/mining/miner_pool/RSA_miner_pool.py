from core.mining.miner_pool.miner_pool import miner_pool
from core.mining.miner.RSA_miner import RSA_miner

class RSA_miner_pool(miner_pool):

    '''Definers a pool of RSA miners'''

    def __init__(self, settings : dict) -> None:
        '''Creates a RSA miner pool'''
        super(RSA_miner_pool, self).__init__(settings)
        
    def get_miner_cls(self):
        '''Returns RSA miner class'''
        return RSA_miner
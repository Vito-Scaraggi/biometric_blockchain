from core.mining.miner_pool.RSA_miner_pool import RSA_miner_pool
from core.mining.miner_pool.ECDSA_miner_pool import ECDSA_miner_pool
from core.users.user_pool.RSA_user_pool import RSA_user_pool
from core.users.user_pool.ECDSA_user_pool import ECDSA_user_pool

class factory:

    '''Cretes miners and users pools for RSA and ECDSA protocol'''

    miner_pools = {
        "RSA" : RSA_miner_pool,
        "ECDSA" : ECDSA_miner_pool
    }

    user_pools = {
        "RSA" : RSA_user_pool,
        "ECDSA" : ECDSA_user_pool
    }

    @staticmethod
    def get_type(settings : dict) -> str:
        '''Returns protocol type from user settings'''
        return settings["general"]["type"]

    @classmethod
    def build_miner_pool(cls, settings : dict):
        '''Creates a miners pool'''
        type = cls.get_type(settings)
        return cls.miner_pools[type](settings)

    @classmethod
    def build_user_pool(cls, settings : dict):
        '''Creates a users pool'''
        type = cls.get_type(settings)
        return cls.user_pools[type](settings)
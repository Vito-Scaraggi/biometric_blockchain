from fastecdsa.curve import secp256k1
from fastecdsa.point import Point

from core.users.user_pool.user_pool import user_pool
from core.users.user.ECDSA_user import ECDSA_user
from core.users.user_flyweight import user_flyweight as uf

class ECDSA_user_pool(user_pool):

    '''Defines a ECDSA users pool'''

    def __init__(self, settings : dict) -> None:
        '''Creates a ECDSA user pool'''
        super(ECDSA_user_pool, self).__init__(settings)
        self.configure_flyweight(settings)
        self.users.sort(key = self.sort_key)
    
    def configure_flyweight(self, settings : dict) -> None:
        '''Configure user flywight in a proper way for ECDSA protocol'''
        super(ECDSA_user_pool, self).configure_flyweight(settings)
        #ecdsa
        uf.n = settings["ECDSA"]["n"]
        uf.q = settings["ECDSA"]["q"]
        uf.Gx = settings["ECDSA"]["Gx"]
        uf.Gy = settings["ECDSA"]["Gy"]
        uf.G = Point( uf.Gx, uf.Gy, curve=secp256k1)
    
    def get_user_cls(self):
        '''Returns ECDSA user class'''
        return ECDSA_user
    
    def sort_key(self, user):
        '''Return user sorting parameter'''
        return user.public_key.param.get("pk")
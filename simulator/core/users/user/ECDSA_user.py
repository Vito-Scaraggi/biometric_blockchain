from random import randrange

from core.users.user.user import user
from core.users.user_flyweight import user_flyweight as uf
from core.util.tools import tools
from core.datastruct.signature import signature
from core.datastruct.public_key import public_key

class ECDSA_user(user):

    '''Defines a user for ECDSA protocol'''

    def __init__(self, id : int) -> None:
        '''Creates a ECDSA user'''
        super(ECDSA_user, self).__init__(id, 'ECDSA')
        self.keygen()

    def keygen(self) -> None:
        '''Generates couple of keys for ECDSA user'''
        fixed_sk = randrange(2,uf.n)
        enrolled_sk = uf.fuzzy_distribution(fixed_sk, uf.w, uf.n)
        noise_term = enrolled_sk - fixed_sk
        pk = enrolled_sk*uf.G
        self.fixed_sk = fixed_sk
        self.public_key = public_key(self.id, {"pk" : pk.x})
        self.enrolled_sk = enrolled_sk
        self.enrolled_noise = noise_term

    def fuzzy_sign(self, message : str) -> tuple:

        '''
        Signs a message.
        Returns signature and respective clearing value.
        '''

        z = tools.hashint(message, uf.mbl)
        sk = uf.fuzzy_distribution(self.fixed_sk, uf.w, uf.n)
        k = randrange(2, uf.n) #k from Zn, but 0,1 are not excluded here? s!= 0??????
        r_point = k*uf.G
        r = (r_point.x)%uf.n
        k_inv = pow(k,uf.n-2,uf.n)
        s = (k_inv*(z+r*sk))%uf.n
        v = (r_point.y)%2
        sig = signature( { "r" : r, "s" : s, "v" : v} )
        clearing = self.enrolled_sk - sk
        return sig, clearing
    
    def get_identity(self) -> int:
        '''Returns ECDSA identity, i.e. number ID'''
        return self.id
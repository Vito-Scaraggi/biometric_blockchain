from math import gcd
from string import ascii_letters, digits
from random import choice, randrange
import rsa

from core.users.user.user import user
from core.users.user_flyweight import user_flyweight as uf
from core.util.tools import tools
from core.datastruct.signature import signature
from core.datastruct.public_key import public_key

class RSA_user(user):
    
    '''Defines a user for RSA protocol'''

    def __init__(self, id : int) -> None:

        '''Creates a RSA user'''

        super(RSA_user, self).__init__(id, 'RSA')
        ul = randrange(8, 17)
        self.username = ''.join([choice(ascii_letters + digits) for _ in range(ul)])
        self.keygen()

    def keygen(self) -> None:
        '''Generates couple of keys for RSA user'''

        (pk, sk) = rsa.newkeys(uf.mbl)
        self.fixed_sk = sk.d
        phi = (sk.p - 1) * (sk.q - 1)
        
        enrolled_sk = uf.fuzzy_distribution(self.fixed_sk, uf.w, pk.n)
        
        flag1 = 0
        flag2 = 0
        cont = 0

        while not (flag1 or flag2):
            cont += 1
            flag1 = gcd( (enrolled_sk - cont) % pk.n, phi) == 1     
            flag2 = gcd( (enrolled_sk + cont) % pk.n, phi) == 1

        if flag1:
            self.enrolled_sk = (enrolled_sk - cont)% pk.n
        else:
            self.enrolled_sk = (enrolled_sk + cont) % pk.n
        
        self.enrolled_noise = self.enrolled_sk - self.fixed_sk
        
        n = pk.n
        e = pow(self.enrolled_sk, -1, phi)
        self.public_key = public_key(self.username, { "n" : n, "e" : e} )

    def fuzzy_sign(self, message : str) -> tuple:
        
        '''
        Signs a message.
        Returns signature and respective clearing value.
        '''

        z = tools.hashint(message, uf.mbl)
        sk = uf.fuzzy_distribution(self.fixed_sk, uf.w, self.public_key.param.get("n"))
        s = pow(z, sk, self.public_key.param.get("n"))
        sig = signature({ "s" : s } )
        clearing = self.enrolled_sk - sk
        return sig, clearing
    
    def get_identity(self) -> str:
        '''Returns ECDSA identity, i.e. username'''
        return self.username
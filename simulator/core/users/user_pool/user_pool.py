from random import choice
from datetime import datetime
from abc import abstractmethod

from core.datastruct.raw_tx import raw_tx
from core.users.user_flyweight import user_flyweight as uf
from core.users.user.user import user
from core.datastruct.public_key import public_key

class user_pool():
    
    '''Defines a pool of users'''

    def configure_flyweight(self, settings : dict) -> None:
        '''Configures user flyweight in a proper way'''
        #general
        uf.mbl = settings["general"]["modulus_bit_length"]
        uf.w =  settings["general"]["w"]
        uf.set_sign(settings["general"]["distr"])
    
    @abstractmethod
    def get_user_cls(*args, **kwargs):
        '''Returns correct user class'''
        pass
     
    def __init__(self, settings : dict) -> None:
        
        '''Creates a pool of users'''

        self.configure_flyweight(settings)
        cl = self.get_user_cls()
        self.users = []
        n_user = settings["general"]["n_users"]
        w = settings["general"]["w"]

        for i in range(n_user):
            flag = True
            while(flag):
                u = cl(i)
                flag = self.is_user_conflict(u, w)
            self.users.append(u)

    def sim_txs(self, num_tx : int) -> list[raw_tx]:

        '''Generates a list of raw transactions'''

        raw_txs = []

        for _ in range(num_tx):
            user = choice(self.users)
            
            username = user.get_identity()
            user_id = user.id

            message = str(datetime.now())
            signature, clearing = user.fuzzy_sign(message)
            raw_txs.append( raw_tx(message, signature, username, user_id, clearing) )
 
        return raw_txs
    
    def is_user_conflict(self, user : user, w : int) -> bool:
        '''
        Check if the last generated user's fuzzy secret key distribution
        intersects other users' fuzzy secret key distribution
        '''
        fsk1 = user.fixed_sk
        flag = False
        for u in self.users:
            fsk2 = u.fixed_sk
            flag |= abs(fsk1 - fsk2) <= 2*w
        return flag
    
    def get_public_file(self) -> list[public_key]:
        '''Returns public file, i.e. a list of public keys'''
        return [ user.public_key for user in self.users]
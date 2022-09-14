from core.users.user_pool.user_pool import user_pool
from core.users.user.RSA_user import RSA_user
from core.users.user_flyweight import user_flyweight as uf

class RSA_user_pool(user_pool):

    '''Defines a RSA users pool'''

    def __init__(self, settings : dict) -> None:
        '''Creates a RSA user pool'''
        super(RSA_user_pool, self).__init__(settings)
    
    def get_user_cls(self):
        '''Returns RSA user class'''
        return RSA_user
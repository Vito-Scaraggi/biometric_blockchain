from abc import abstractmethod

class user():

    '''Defines a blockchain user'''

    @abstractmethod
    def keygen(*args, **kwargs):
        '''Generate a couple of keys'''
        pass
    
    @abstractmethod
    def fuzzy_sign(*args, **kwargs):
        '''Signs a message'''
        pass
    
    @abstractmethod
    def get_identity(*args, **kwargs):
        '''Returns user identity'''
        pass
    
    def __init__(self, id : int, type : str) -> None:
        '''Creates a user with given id and type'''
        self.id = id
        self.type = type
        
    def __str__(self) -> str:
        '''Returns user info string'''
        
        s = "Identity : {}\n\n".format(self.get_identity())
        s+= "Fixed secret key :\n\t{}\n\nNoise when enrolling :\n\t{}\n\nEnrolled secret key :\n\t{}\n\nEnrolled public key : {}\n".format(
                                                                hex(self.fixed_sk), 
                                                                str(self.enrolled_noise), 
                                                                hex(self.enrolled_sk), 
                                                                str(self.public_key)
                                                            )
        return s
from dataclasses import dataclass

from core.datastruct.signature import signature

@dataclass(frozen=True)
class raw_tx:

    '''Defines the structure of a raw transaction'''

    message : str
    signature: signature
    username : str
    user_id : int
    clearing : int

    def get_identity(self):
        '''Returns identity parameter'''
        return self.username
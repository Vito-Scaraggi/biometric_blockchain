import json

from core.util.tools import tools
from core.datastruct.raw_tx import raw_tx

class block:
    
    '''Defines the structure of a block'''

    def __init__(self, aux : str, block_number : int, difficulty : int, nonce : str, seed_values : list[int], raw_txs : list[raw_tx]):
        '''Creates a block'''

        numTx = len(raw_txs)
        self.header = {'parentHash':aux, 'blockNumber':block_number, 
                        'NumTx': numTx, 'difficulty': difficulty, 'nonce': nonce}; 
        
        if difficulty is None:
            self.header.pop('difficulty')
        
        self.body = []
        
        for i in range(numTx):
            m = raw_txs[i].message
            identity = raw_txs[i].get_identity()
            signature = raw_txs[i].signature.get_hex_param()
            mined_tx = {'Tx#':i, 'identity': identity, 'timestamp': m, 'signature' : signature, "PoW" : seed_values[i]} 
            self.body.append(mined_tx)

    def to_json(self):
        '''Returns an array with block header and block body'''
        return [self.header, self.body]

    def __str__(self):
        '''Converts block to a readable json string'''
        return json.dumps(self.to_json(), indent = 4)
    
    def __hash__(self):
        '''Returns block hash'''
        return tools.hash(str(self))
from random import randrange
from math import log2, ceil

from core.datastruct.packet import packet
from core.datastruct.block import block
from core.util.tools import tools

class miner_flyweight:

    '''
    Defines a flyweight for miner classes.
    It contains methods and attributes shared by all miner istances.
    It's configured by miner pool classes.
    '''

    @classmethod
    def range_conversion(cls, digest_val_binary : list[int] ) -> int:
        '''Converts binary array into an integer value between -2w and 2w'''
        bit_sign = 2*int(digest_val_binary[0],2)-1;
        num_bits = 1+ceil(log2(cls.w));
        absolute_value = (int(digest_val_binary[1:1+num_bits],2))%(2*cls.w);
        delta_e = (bit_sign*absolute_value)
        return delta_e;

    @classmethod
    @tools.crono
    def classical_pow(cls, packet : packet, seed_values : list[int]) -> tuple:
        
        '''Makes classical Proof of Work'''

        aux = packet.aux
        block_number = packet.block_number
        raw_txs = packet.raw_txs
        delta_num_tx = cls.max_tx - len(raw_txs)
        n_attempts = 0
        nonce = ''

        if delta_num_tx == 0:
            difficulty = 0
        else:
            ell = cls.base_diff + ceil(log2((4*cls.w+1)*delta_num_tx))
            difficulty = ell

        b = block(aux, block_number, difficulty, nonce, seed_values, raw_txs)

        if difficulty:            
            flag_PoW = 0

            while not flag_PoW:
                n_attempts+=1
                nonce = hex(randrange(2**cls.hashl))
                b.header["nonce"] = nonce
                flag_PoW = cls.verify_nonce(b)

        return n_attempts, b

    @classmethod
    def verify_nonce(cls, b : block) -> bool:
        '''Checks if block nonce is valid'''
        hash = b.__hash__()
        nonce = b.header.get("nonce")
        diff = b.header.get("difficulty")
        digest_input = hash + nonce;   
        digest_val = tools.hashint(digest_input)
        digest_val_binary = format(digest_val, "08b").zfill(cls.hashl);
        flag_PoW = digest_val_binary.startswith("0" * diff)
        return flag_PoW
    
    @classmethod
    def auth(cls, test : int, target : int, delta : int) -> bool:
        '''
        Makes an authentication attempt.
        Checks if test value is equal to target and clearing value is valid.
        '''
        return test == target and -2*cls.w <= delta <= 2*cls.w
    
    @classmethod
    def ident(cls, test : int, public_file : list[int], delta : int) -> bool:
        '''
        Makes an identification attempt.
        Checks if test value is in target list and clearing value is valid.
        '''
        target_list = [ p.param.get("pk") for p in public_file]
        ok = test in target_list and -2*cls.w <= delta <= 2*cls.w
        return ok
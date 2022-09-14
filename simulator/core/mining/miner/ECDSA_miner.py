from fastecdsa.curve import secp256k1
from fastecdsa.point import Point
from fastecdsa.util import mod_sqrt
from random import randrange

from core.mining.miner.miner import miner
from core.mining.miner_flyweight import miner_flyweight as mf
from core.mining.sync_buffer import sync_buffer
from core.datastruct.signature import signature
from core.datastruct.public_key import public_key
from core.util.tools import tools

class ECDSA_miner(miner):

    '''Defines a miner for ECDSA blockchain protocol'''
    
    def __init__(self, id : int, evil : bool, sbuffer : sync_buffer) -> None:
        '''Creates a ECDSA miner'''
        super(ECDSA_miner, self).__init__(id, 'ECDSA', evil, sbuffer)

    def compute_verifying(self, message: str, signature : signature, public_key : public_key = None) -> Point:
        
        '''Computes the non fuzzy verifying public key'''

        r = signature.param.get("r")
        s = signature.param.get("s")
        v = signature.param.get("v")
        
        z = tools.hashint(message, mf.mbl)
        
        r_cube = pow(r,3,mf.q);
        y_of_r = mod_sqrt(r_cube+7, mf.q);

        if y_of_r[0]%2 == v:
            y_of_r = y_of_r[0];
        else:
            y_of_r = y_of_r[1];

        k_mul_G = Point(r, y_of_r, curve=secp256k1);
        
        r_inv = pow(r,mf.n-2,mf.n);
        s_mul_k_G = s*k_mul_G;
        verifying_pk = r_inv*(s_mul_k_G - z*mf.G);

        return verifying_pk;

    def clear_attempt(self, message: str, aux : str, ver_pk : Point, 
                        public_file : list[public_key], public_key: public_key, 
                        PoW : str = None) -> tuple:

        '''
            Makes a fair clearing attempt.
            First step is PRNG phase.
            Second step is CRYPTO phase.
            Then it checks if cleared public key appears in public file.
        '''
        
        eta_prng, test_seed, test_delta_e = self.prng_phase(message, aux, public_key, PoW)
        eta_crypto, test_pk = self.crypto_phase(test_delta_e, ver_pk)
        ok = mf.ident(test_pk.x, public_file, test_delta_e)
        return eta_prng, eta_crypto, ok, test_seed;

    @tools.crono
    def prng_phase(self, m : str, aux : str, public_key : public_key, PoW : str = None) -> tuple:

        '''Executes PRNG phase as described in ECDSA blockchain protocol.'''

        test_seed = hex(randrange(2**mf.mbl)) if PoW is None else PoW;
        prng_input = m + test_seed + aux;
        digest_val = tools.hashint(prng_input, mf.mbl)
        digest_val_binary = format(digest_val, "0" + str(mf.mbl) + "b")
        
        for _ in range(mf.prng_X):

            delta_e_all = int(digest_val_binary,2)%mf.n;        
            point = delta_e_all*mf.G + mf.G_;
            digest_val = tools.hashint(hex(point.x), mf.mbl)
            digest_val_binary = format(digest_val, "0" + str(mf.mbl) + "b")

        test_delta_e =  mf.range_conversion(digest_val_binary)
        return test_seed, test_delta_e

    @tools.crono
    def crypto_phase(self, delta : int, c : Point) -> tuple[int]:

        '''Executes CRYPTO phase as described in ECDSA blockchain protocol.'''
        
        return (c + delta*mf.G, )
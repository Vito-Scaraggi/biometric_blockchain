from random import randrange

from core.mining.miner.miner import miner
from core.mining.miner_flyweight import miner_flyweight as mf
from core.mining.sync_buffer import sync_buffer
from core.datastruct.signature import signature
from core.datastruct.public_key import public_key
from core.util.tools import tools

class RSA_miner(miner):

    '''Defines a miner for RSA blockchain protocol'''

    def __init__(self, id : int, evil : bool, sbuffer : sync_buffer) -> None:
        
        '''Creates a RSA miner'''

        super(RSA_miner, self).__init__(id, "RSA", evil, sbuffer)

    def compute_verifying(self, message : str, signature : signature, public_key : public_key ) -> tuple[int]:

        '''Computes the hash of the message and the non-fuzzy verifying signature'''

        s = signature.param.get("s")
        e = public_key.param.get("e")
        n = public_key.param.get("n")
        ver_s = pow(s, e, n)
        hash_m = tools.hashint(message) % n
        return ver_s, hash_m

        
    def clear_attempt(self, message : str, aux : str, ver : tuple[int], 
                        public_file : list[public_key], public_key : public_key,
                        PoW : str = None) -> tuple:
        
        '''Makes a fair clearing attempt'''

        eta_prng, test_seed, test_delta_e = self.prng_phase(message, aux, PoW)
        ver_s , hash_m = ver[0], ver[1]
        eta_crypto, test_m = self.crypto_phase(test_delta_e, ver_s, hash_m, public_key)
        ok = mf.auth(test_m, hash_m, test_delta_e)
        return eta_prng, eta_crypto, ok, test_seed;

    @tools.crono
    def prng_phase(self, m : str, aux : str, PoW : str = None) -> tuple:
        
        '''Executes PRNG phase as described in RSA blockchain protocol.'''

        #n = public_key.param.get("n")
        test_seed = hex(randrange(2**mf.mbl)) if PoW is None else PoW
        prng_input = m + test_seed + aux
        digest_val = tools.hashint(prng_input, mf.mbl)
        digest_val_binary = format(digest_val, "0" + str(mf.mbl) + "b")

        for _ in range(mf.prng_X):
            seed = int(digest_val_binary, 2) % mf.prng_n
            y = (mf.prng_b * pow(mf.prng_a, seed, mf.prng_n)) % mf.prng_n
            digest_val = tools.hashint( hex(y), mf.mbl)
            digest_val_binary = format(digest_val, "0" + str(mf.mbl) + "b")

        test_delta_e =  mf.range_conversion(digest_val_binary)
        return test_seed, test_delta_e

    @tools.crono
    def crypto_phase(self, delta : int, y : int, z : int, public_key : public_key) -> tuple[int]:

        '''Executes CRYPTO phase as described in RSA blockchain protocol.'''

        n = public_key.param.get("n")
        e  = public_key.param.get("e")
        return ( (y * pow(z, delta * e, n) ) % n, )
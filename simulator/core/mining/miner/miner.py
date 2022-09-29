from abc import abstractmethod
from multiprocessing import Process
from random import seed

from core.stats.block_stats import block_stats
from core.datastruct.public_key import public_key
from core.datastruct.packet import packet
from core.datastruct.signature import signature
from core.mining.miner_flyweight import miner_flyweight as mf
from core.mining.sync_buffer import sync_buffer
from core.util.tools import tools

class miner(Process):
    
    '''Defines a miner process.'''

    @abstractmethod
    def compute_verifying(self, message: str, signature : signature, public_key : public_key):
        '''Makes some computations needed by clearing process'''
        pass

    @abstractmethod
    def clear_attempt(self, message: str, aux : str, ver, 
                        public_file : list[public_key], public_key: public_key, 
                        PoW : str) -> tuple:
        '''Makes a fair clearing attempt'''
        pass
    
    @abstractmethod
    def prng_phase(self, message : str, aux : str, public_key : public_key, PoW : str) -> tuple:
        '''Executes PRNG phase'''
        pass

    @abstractmethod
    def crypto_phase(*args, **kwargs) -> tuple[int]:
        '''Executes CRYPTO phase'''
        pass
    
    def  __init__(self, id : int, type : str, evil : bool, sbuffer : sync_buffer) -> None:
        
        '''Creates a miner process'''

        super(miner,self).__init__()
        
        self.id = id
        self.type = type
        self.sbuffer = sbuffer
        self.evil = evil
        self.desc = "Evil" if evil else "Fair"
    
    def run(self) -> None:

        '''Executes miner's task'''
        seed(self.id)
        packet = self.sbuffer.get_packet()
        bs = block_stats(packet.raw_txs)
        seed_values = []
        num_tx = len(packet.raw_txs)
        
        for i in range(num_tx):

            eta, eta_prng, eta_crypto, n_attempts, test_seed = self.clear_tx(packet, i)
            
            seed_values.append(test_seed)
            
            bs.tx_times.append(eta)
            bs.tx_attempts.append(n_attempts)
            bs.prng_times.append(eta_prng)
            bs.crypto_times.append(eta_crypto)
            
            msg = "[{} Miner:{}]".format(self.desc, self.id) + " Transaction #{} mined".format(i)

            self.sbuffer.put_log(msg)
        
        eta, n_attempts, b = mf.classical_pow(packet, seed_values)


        bs.cpow_attempts = n_attempts
        bs.cpow_time = eta
        bs.evil = self.evil
        bs.num_tx = num_tx
        bs.miner_id = self.id

        msg = "[{} Miner:{}] Classical Pow finished".format(self.desc, self.id)
        self.sbuffer.put_log(msg)
        
        self.sbuffer.before_produce()
        bs.raw_block = str(b)
        self.sbuffer.after_produce(b, bs)
    
    @tools.crono
    def clear_tx(self, packet : packet, tx_id : int) -> tuple:
        
        '''Clear a raw transaction'''

        n_attempts = 0
        eta_prng = 0
        eta_crypto = 0

        message = packet.raw_txs[tx_id].message
        aux = packet.aux
        public_file = packet.public_file
        user_id = packet.raw_txs[tx_id].user_id
        public_key = public_file[user_id]

        flag_cleared = 0

        if self.evil:
            clearing = packet.raw_txs[tx_id].clearing
            
            while flag_cleared == 0:
                n_attempts += 1;
                prng_time, flag_cleared, test_seed = self.evil_clear_attempt(message, aux, clearing);
                eta_prng += prng_time
        else:
            signature = packet.raw_txs[tx_id].signature
            ver = self.compute_verifying(message,signature, public_key)
            while flag_cleared == 0:
                n_attempts += 1;
                prng_time, crypto_time, flag_cleared, test_seed = self.clear_attempt(message,aux,ver,public_file, public_key);
                eta_prng += prng_time
                eta_crypto += crypto_time
        
        return eta_prng, eta_crypto, n_attempts, test_seed
    
    def evil_clear_attempt(self, message : str, aux: str, clearing : int) -> tuple:
        '''Makes an evil clearing attempt'''
        eta_prng, test_seed, test_delta_e = self.prng_phase(message, aux)
        ok = mf.auth(test_delta_e, clearing, test_delta_e)
        return eta_prng, ok, test_seed;
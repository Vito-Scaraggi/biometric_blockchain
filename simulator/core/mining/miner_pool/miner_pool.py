from abc import abstractmethod
from random import shuffle, choice

from core.datastruct.packet import packet
from core.datastruct.signature import signature
from core.datastruct.block import block
from core.datastruct.public_key import public_key
from core.mining.miner_flyweight import miner_flyweight as mf
from core.mining.miner.miner import miner
from core.mining.sync_buffer import sync_buffer

class miner_pool():
    
    '''Defines a pool of miners'''

    @abstractmethod
    def get_miner_cls(self):
        '''Returns miner class'''
        pass
    
    def __init__(self, settings : dict) -> None:
        '''Creates a miner pool and configures miner flyweight'''

        self.n_miner = settings["general"]["n_miners"]
        self.evil_miner = settings["general"]["n_evils"]
        self.configure_flyweight(settings)
    
    def start_mining(self, packet : packet) -> tuple:
        
        '''
        Setups miner pool when a new packet arrives.
        Then it waits until a miner finishes Proof of Work and presents a block.
        If block is valid, it terminates all miner processes,
        otherwise it waits for a new block.
        It also retrieves logs.
        '''

        cls = self.get_miner_cls()
        sbuffer = sync_buffer()
        
        evil = [ cls( _, True, sbuffer) for _ in range(self.evil_miner)]
        fair = [ cls( _, False, sbuffer) for _ in range(self.n_miner - self.evil_miner)]
        
        miners = fair + evil
        shuffle(miners)
        
        sbuffer.send_packets(packet, self.n_miner)

        for m in miners:
            m.start()

        ok = False
    

        while(not ok):
            
            block, stats, logs = sbuffer.before_consume()
            ok =  self.accept_block(miners, block, packet.public_file)
            msg = "Block accepted\n" if ok else "Block denied\n"
            logs += [msg]
            
            if ok:
                for m in miners:
                    m.terminate()
                    m.join()
                    m.close()

            sbuffer.after_consume()
        
        stats.logs = logs
        return block, stats
    
    def configure_flyweight(self, settings : dict) -> None:
        '''Configures miner flyweight'''
        mf.hashl = 256
        #general
        mf.mbl = settings["general"]["modulus_bit_length"]
        mf.base_diff = settings["general"]["base_diff"]
        mf.max_tx = settings["general"]["max_tx"]
        mf.w =  settings["general"]["w"]
        #prng
        mf.prng_a = settings["PRNG"]["a"]
        mf.prng_b = settings["PRNG"]["b"]
        mf.prng_X = settings["PRNG"]["X"]
    
    def accept_block(self, miners : list[miner], block : block, public_file : list[public_key]) -> bool:
        
        '''Establishes if given block is valid'''

        miner = choice(miners)
        aux = block.header["parentHash"]
        
        accept = True

        for tx in block.body:
            m = tx["timestamp"]
            s = signature( { key : int(val, 16) for key, val in tx["signature"].items() } )
            pk = [p for p in public_file if p.identity == tx["identity"]][0]
            ver = miner.compute_verifying(m, s, pk)
            PoW = tx["PoW"]
            tmp1, tmp2, ok, tmp3 = miner.clear_attempt(m, aux, ver, public_file, pk, PoW)
            accept &= ok
        
        diff = block.header.get("difficulty")
        
        if accept and diff:
            accept &= mf.verify_nonce(block)

        return accept
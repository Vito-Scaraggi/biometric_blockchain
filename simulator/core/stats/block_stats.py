from datetime import timedelta
from dataclasses import dataclass, field

from core.datastruct.raw_tx import raw_tx

@dataclass
class block_stats:

    '''Defines statistics referred to a block'''
    
    raw_txs : list[raw_tx]
    raw_block : str = field(init=False)
    miner_id : int = field(init=False)
    evil : bool = field(init=False)
    num_tx : int = field(init=False)
    tx_times : list[float] = field(default_factory=list)
    prng_times : list[float] = field(default_factory=list)
    crypto_times : list[float] = field(default_factory=list)
    tx_attempts : list[int] = field(default_factory=list)
    cpow_time : float = field(init=False)
    cpow_attempts : int = field(init=False)
    logs : list[str] = field(default_factory=list)

    def get_info(self, index : int) -> str:
        
        '''Returns info string referred to specific block'''

        return "Block number: #{}\nMiner ID: {}\nType: {}\nNumber of Tx: {}\nCreation time: {}".format(
            index,
            self.miner_id,
            "evil" if self.evil else "fair",
            self.num_tx,
            timedelta(seconds = sum(self.tx_times) + self.cpow_time)
        )

    def get_logs(self):

        '''Returns all logs'''

        return "\n".join(self.logs)
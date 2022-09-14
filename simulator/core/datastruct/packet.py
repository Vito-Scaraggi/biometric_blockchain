from dataclasses import dataclass
from core.datastruct.public_key import public_key
from core.datastruct.raw_tx import raw_tx

@dataclass(frozen=True)
class packet:
    '''Represents a packet which contains mining useful information'''
    block_number : int
    aux : int
    raw_txs : list[raw_tx]
    public_file : list[public_key]
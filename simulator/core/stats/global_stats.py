from dataclasses import dataclass, field
from datetime import timedelta
from numpy import ndarray

@dataclass
class global_stats:

    '''Defines simulation statistics'''

    sim_time : timedelta = field(init=False)
    avg_bc_time : timedelta = field(init=False)
    count_block : ndarray  = field(init=False)
    avg_tx_time : ndarray = field(init=False)
    avg_tx_p_time : ndarray = field(init=False)
    avg_tx_c_time : ndarray = field(init=False)
    avg_tx_attempts : ndarray = field(init=False)
    avg_cpow_time : ndarray = field(init=False)
    avg_cpow_attempts : ndarray = field(init=False)
    avg_p_c_ratio : ndarray = field(init=False)
    avg_cr_time : ndarray = field(init=False)
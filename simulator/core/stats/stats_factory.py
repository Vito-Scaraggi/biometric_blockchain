from typing import Callable
from numpy import zeros, ndarray, vectorize
from datetime import timedelta

from core.stats.global_stats import global_stats
from core.stats.block_stats import block_stats

class stats_factory:
    
    '''Generates statistics'''

    def __init__(self) -> None:
        '''Creates an array of block statistics'''

        self.block_stats = []

    def put(self, new_stats : block_stats) -> None:
        '''Append new block statistics to array'''
        self.block_stats.append(new_stats)

    def cond(bs : block_stats, b : bool, t : int) -> bool:
        '''
        Check if block was mined by evil/fair miner
        and contains given number of transactions
        '''
        return bs.evil == b and bs.num_tx == t

    def get_value(self, o : object, prop : str):
        '''Returns object property if present'''
        if prop:
            return getattr(o, prop)
        return None

    def matrix(self, func : Callable, max_tx : int, prop : str = None) -> ndarray:
        '''
        Builds a statistics matrix.
        Rows represents evil or fair types.
        Columns represents number of transactions.
        ''' 
        matrix = zeros( [3, max_tx+1] )

        for b in [False, True]:
            for t in range(1, max_tx + 1):
                matrix[b+1, t] = sum( [ func( self.get_value(bs, prop) )  
                                        for bs in self.block_stats if stats_factory.cond(bs, b, t) ] )

        for t in range(1, max_tx+1):
            matrix[0 , t] = sum(matrix[: , t])

        for b in range(1, 3):
            matrix[b , 0] = sum(matrix[b, :])

        matrix[0, 0] = sum(matrix[ : , 0])
        return matrix

    def custom_divide(mat1 : ndarray, mat2 : ndarray, digs : int) -> ndarray:

        '''
        Divide two matrix element-wise.
        Division result has given number of decimal digits.
        '''

        shape_1 = mat1.shape
        shape_2 = mat2.shape

        if shape_1 == shape_2:
            
            x = shape_1[0]
            y = shape_1[1]

            ret = zeros( [x,y] )

            for b in range(x):
                for t in range(y):
                    ret[b, t] = round(mat1[b, t] / mat2[b, t], digs) if mat2[b,t] > 0 else 0

        return ret

    def calc(self, sim_time : float, max_tx : int) -> global_stats:

        '''Calculates simulation statistics'''

        g_stats = global_stats()
        g_stats.sim_time = timedelta( seconds = sim_time)
        
        count_block = self.matrix( lambda x: 1, max_tx)
        tx_time = self.matrix( lambda x: sum(x), max_tx, "tx_times")
        tx_p_time = self.matrix( lambda x: sum(x), max_tx, "prng_times")
        tx_c_time = self.matrix( lambda x: sum(x), max_tx, "crypto_times")
        tx_attempts = self.matrix( lambda x: sum(x), max_tx, "tx_attempts")
        cpow_time = self.matrix( lambda x: x, max_tx, "cpow_time")
        cpow_attempts = self.matrix( lambda x: x, max_tx, "cpow_attempts")
        
        g_stats.count_block = count_block
        g_stats.avg_tx_time = stats_factory.custom_divide(tx_time, count_block, 3)
        g_stats.avg_tx_p_time = stats_factory.custom_divide(tx_p_time, count_block, 3)
        g_stats.avg_tx_c_time = stats_factory.custom_divide(tx_c_time, count_block, 3)
        g_stats.avg_tx_attempts = stats_factory.custom_divide(tx_attempts, count_block, 0)
        g_stats.avg_cpow_time = stats_factory.custom_divide(cpow_time, count_block, 3)
        g_stats.avg_cpow_attempts = stats_factory.custom_divide(cpow_attempts, count_block, 0)
        g_stats.avg_p_c_ratio = stats_factory.custom_divide(tx_p_time, tx_c_time, 3)
        avg_cr_time = g_stats.avg_tx_time + g_stats.avg_cpow_time
        round3 = vectorize(lambda x : round(x, 3))
        g_stats.avg_cr_time = round3(avg_cr_time)
        
        return g_stats
from core.stats.stats_factory import stats_factory
from core.util.json import json_alias
from core.users.user_pool.user_pool import user_pool
from core.stats.block_stats import block_stats

class report:

    '''Defines a simulation report'''
    
    def __init__(self, settings : dict, user_pool : user_pool) -> None:

        '''Creates a report'''

        self.settings = settings
        self.user_pool = user_pool
        self.stats_f = stats_factory()

    def put_stats(self, new_stats : block_stats) -> None:

        '''Stores new block statistics'''

        self.stats_f.put(new_stats)

    def get_stats(self, sim_time : float ) -> None:

        '''Generates and saves statistics'''        
        
        max_tx = self.settings["general"]["max_tx"]
        self.stats = self.stats_f.calc(sim_time, max_tx)
    
    def get_info(self) -> str:

        '''Returns info string containing simulation settings'''

        info = "" 
        info += "Elapsed time: {}\n".format( self.stats.sim_time )
        info += "Average block creation time: {}\n\n".format(self.stats.avg_bc_time)
        
        sections = ["general", "PRNG", self.settings["general"]["type"]]

        for s in sections:
                props = self.settings.get(s)
                if props:
                    for p in props:
                        info += "{}: {}\n".format( json_alias[s][p], self.settings[s][p])
                    info += "\n"
        
        return info
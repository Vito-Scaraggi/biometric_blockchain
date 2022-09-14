from core.stats.report import report
from core.util.factory import factory
from gui.gui import Gui
from core.datastruct.packet import packet
from core.util.tools import tools

class blockchain:

    '''Defines a blockchain'''

    def __init__(self, settings : dict) -> None:

        '''Creates blockchain'''
        
        super(blockchain, self).__init__()

        self.type = settings["general"]["type"]
        self.n_blocks = settings["general"]["n_blocks"]
        self.max_tx = settings["general"]["max_tx"]
        self.blocks = []
        
        print("Initializing user pool", end = " ... ")
        self.miner_pool = factory.build_miner_pool(settings)
        print("User pool initialized")
        print("Initializing miner pool", end = " ... ")
        self.user_pool = factory.build_user_pool(settings)
        print("Miner pool initialized")

        self.report = report(settings, self.user_pool)

    def start(self) -> None:
        '''Starts blockchain'''
        eta = self.simulate()[0]
        self.report.get_stats(eta)
        Gui(self.report)

    @tools.crono
    def simulate(self) ->None:
        
        '''Simulates blockchain'''

        public_file = self.user_pool.get_public_file()

        for block_number in range(1,self.n_blocks+1):
            print("Creating block {}/{}".format(block_number, self.n_blocks), end = " ... ")
            aux = self.retrieve_aux()
            raw_txs = self.user_pool.sim_txs( (block_number % self.max_tx) + 1)
            p = packet(block_number, aux, raw_txs, public_file)
            
            block, stats = self.miner_pool.start_mining(p)
            self.blocks.append(block)
            self.report.put_stats(stats)
            print("Block created")
        
        return ()

    def retrieve_aux(self) -> str:
        
        '''Retrieve auxiliary string or parentHash'''

        if not self.blocks:
            return "0x0000000000000000000"
        else:
            last = len(self.blocks) - 1
            return self.blocks[last].__hash__()
from multiprocessing import Queue, Semaphore

from core.datastruct.packet import packet

class sync_buffer:
    
    '''
        Implements producer-consumer logic for miner process synchronization.
    '''

    def __init__(self) -> None:
        '''
        Setups synchronization primitives and queues.
        Creates semaphores free and item.
        Creates four queues for blocks, packets, stats and logs.
        '''
        self.mined_queue = Queue()
        self.packet_queue = Queue()
        self.stats_queue = Queue()
        self.logs_queue = Queue()

        self.free = Semaphore(1)
        self.item = Semaphore(0)

    def send_packets(self, packet : packet, n : int) -> None:
        '''
        Inserts packets in packet queue.
        '''
        for _ in range(n):
            self.packet_queue.put(packet)

    def before_consume(self) -> tuple:
        '''
            Miner pool gets block, stats and logs from respective queues
        '''
        self.item.acquire()
        block = self.mined_queue.get()
        stats = self.stats_queue.get()
        logs = []
        while not self.logs_queue.empty():
                logs.append(self.logs_queue.get())
        return block, stats, logs
    
    def after_consume(self) -> None:
        '''
            Miner pool releases queues
        '''
        self.free.release()

    def get_packet(self) -> None:
        '''Miner gets packet from packet queue'''
        return self.packet_queue.get()

    def put_log(self, log) -> None:
        '''Miner puts log into logs queue'''
        self.logs_queue.put(log)

    def before_produce(self) -> None:
        '''Miner acquires block queue'''
        self.free.acquire()
        
    def after_produce(self, block, block_stats) -> None:
        '''Miner puts block and stats into respective queues and releases them'''
        self.mined_queue.put(block)
        self.stats_queue.put(block_stats)
        self.item.release()
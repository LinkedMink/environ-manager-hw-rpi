import logging
from queue import Queue, Empty
from threading import Thread
from time import sleep

class BatchEntityPersister(Thread):
    """Save entities to a database as a batch. This thread will receive new
    records on a shared queue. When a limit is reached, the entities will
    be flushed to the database. 
    """

    MIN_BATCH_SIZE = 10
    CHECK_INTERVAL = 15
    logger = logging.getLogger('BatchEntityPersister')

    def __init__(self, repository, entry_queue, type = 'Entity'):
        super(BatchEntityPersister, self).__init__()
        self.repository = repository
        self.entry_queue = entry_queue
        self.type = type
        self.is_running = False

    def flush(self):
        if self.entity_buffer is None:
            return
            
        BatchEntityPersister.logger.info(
            'Saving Batch of {0}: {1}'.format(self.type, len(self.entity_buffer)))

        try:
            self.repository.add(self.entity_buffer)
        except Exception as e:
            BatchEntityPersister.logger.error(e)

        self.entity_buffer.clear()

    def dequeue_all(self):
        while True: 
            try:
                item_dequeued = self.entry_queue.get(False)
                BatchEntityPersister.logger.debug('Item Dequeued: {0}'.format(item_dequeued))
            except Empty:
                BatchEntityPersister.logger.debug('dequeue_all: Empty')
                break

            if item_dequeued != None:
                self.entity_buffer.append(item_dequeued)

    def run(self):
        self.entity_buffer = []

        self.is_running = True
        while self.is_running:
            sleep(BatchEntityPersister.CHECK_INTERVAL)

            self.dequeue_all()

            if len(self.entity_buffer) > BatchEntityPersister.MIN_BATCH_SIZE:
                self.flush()

    def stop(self):
        self.is_running = False
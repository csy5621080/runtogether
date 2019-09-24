import multiprocessing
import uuid
from runtogether.worker_types import DEFAULT_WSGI
from runtogether.utils import WorkerBaseQueue


class CBaseProcess(multiprocessing.Process):

    def __init__(self, app, workers, queue=WorkerBaseQueue, host='0.0.0.0', port=0, worker_type=DEFAULT_WSGI):
        self.host = host
        self.port = port
        self.app = app
        self.queue = queue(workers)
        self.name = 'WorkerProcess[%s]' % str(uuid.uuid4())
        super(CBaseProcess, self).__init__(target=worker_type, args=(self, ))
import multiprocessing


class WorkerBaseQueue(object):
    _lock = multiprocessing.Lock()

    def __init__(self, workers):
        self.workers = workers

    def __new__(cls, *args, **kwargs):
        if not hasattr(WorkerBaseQueue, "_instance"):
            with WorkerBaseQueue._lock:
                if not hasattr(WorkerBaseQueue, "_queue"):
                    WorkerBaseQueue._queue = multiprocessing.Queue(args[0])
        return WorkerBaseQueue._queue

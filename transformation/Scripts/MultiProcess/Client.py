import multiprocessing as mp
from multiprocessing.managers import SyncManager
import queue
from .Worker import WorkerManager


def MakeClientManager(host, port, authkey):
    """Create a manager for the client. This manager will connect to a server and get the shared queues"""

    class ServerQueueManager(SyncManager):
        pass

    ServerQueueManager.register('get_job_q')
    ServerQueueManager.register('get_result_q')

    manager = ServerQueueManager(address=(host, port), authkey=authkey.encode('utf-8'))
    manager.connect()

    print ('Client connected to {}:{}'.format(host, port))
    return manager


def RunClient(mp_job_worker, host, port, authkey):
    """The function that connect to the server and start to process the jobs. OutputDir is the path to the local output directory. mp_job_worker the function that take the input_queue and the results_queue and process the results."""
    manager = MakeClientManager(host, port, authkey)

    job_q = manager.get_job_q()
    result_q = manager.get_result_q()

    #Do the job (only one process)
    WorkerManager(mp_job_worker, job_q, result_q)

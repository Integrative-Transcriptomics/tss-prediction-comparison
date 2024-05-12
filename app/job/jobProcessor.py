from .jobStatus import jobStatus

def jobProcessor(queue):
    while True:
        job = queue.get()
        job.status = jobStatus.RUNNING
        job.process()
        queue.task_done()


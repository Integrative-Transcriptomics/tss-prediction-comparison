from app.job.JobStatus import JobStatus


# job processing thread, does nothing unless queue contains element, the processes queue elements
def job_processor(queue):
    while True:
        job = queue.get()
        job.status = JobStatus.RUNNING
        job.process()
        queue.task_done()

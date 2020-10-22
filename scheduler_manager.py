import threading
from queue import PriorityQueue
from models.job_type import JobType
from models.job import Job
import datetime
class SchedulerManager(object):
    def __init__(self, threads):
        self.number_of_threads = threads
        self.queue_lock = threading.RLock()
        self.thread_lock = threading.RLock()
        self.jobs_queue = []
        self.current_threads = 0
        self.jobs_thread = threading.Thread(target=self.execute_jobs)
        self.jobs_thread.start()

    def update_thread_count(self, step):
        with self.thread_lock:
            self.current_threads += step


    def can_launch_thread(self):
        with self.thread_lock:
            return self.current_threads < self.number_of_threads

    def get_job(self):
        with self.queue_lock:
            if self.jobs_queue[-1][0] <= datetime.datetime.now():
                print(self.jobs_queue[-1][0], datetime.datetime.now())
                return self.jobs_queue.pop()
            return None

    def is_queue_empty(self):
        with self.queue_lock:
            return len(self.jobs_queue) <= 0

    def add_to_queue(self, job, timestamp):
        print("adding to queue")
        with self.queue_lock:
            self.jobs_queue.append([timestamp, job])
            self.jobs_queue.sort(key=lambda x: x[0], reverse=True)
        print("added to queue")

    def execute_jobs(self):
        print("executing jobs")
        while True:
            if not self.is_queue_empty():
                job = self.get_job()
                if job and self.can_launch_thread():
                    thread = threading.Thread(target=self.execute, args=([job[1]]))
                    thread.start()
                    self.update_thread_count(1)


    def execute(self, job):
        print("executing job", job)
        if job.job_type == JobType.ADHOC:
            job.run()
        elif job.job_type == JobType.SCHEDULED:
            now = datetime.datetime.now()
            self.add_to_queue(job, now+job.duration)
            job.run()
        elif job.job_type == JobType.DELAYED:
            job.run()
            now = datetime.datetime.now()
            self.add_to_queue(job, now+job.duration)
        self.update_thread_count(-1)

    def schedule(self, executable, job_type, time=None, duration=None):
        if job_type == JobType.ADHOC:
            if not time:
                return
            job = Job(executable, job_type)
            self.add_to_queue(job, time)

        elif job_type == JobType.DELAYED:
            if not duration:
                return
            time_stamp = datetime.datetime.now()
            job = Job(executable, job_type, duration=duration)
            self.add_to_queue(job, time_stamp)

        elif job_type == JobType.SCHEDULED:
            if not duration:
                return
            time_stamp = datetime.datetime.now()
            job = Job(executable, job_type, duration=duration)
            self.add_to_queue(job, time_stamp)



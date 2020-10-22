class Job(object):
    def __init__(self, executable, job_type, duration=None):
        self.executable = executable
        self.job_type = job_type
        self.duration = duration

    def run(self):
        self.executable()

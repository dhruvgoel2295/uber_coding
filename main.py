# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from scheduler_manager import SchedulerManager
from models.job_type import JobType
import datetime

def main():
    scheduler = SchedulerManager(5)
    scheduler.schedule(job1, JobType.ADHOC, time=datetime.datetime.now() + datetime.timedelta(seconds=1))
    scheduler.schedule(job2, JobType.ADHOC, time=datetime.datetime.now() + datetime.timedelta(seconds=5))
    scheduler.schedule(job3, JobType.ADHOC, time=datetime.datetime.now() + datetime.timedelta(seconds=10))

def job1():

    print("job1", datetime.datetime.now())

def job2():
    print("job2", datetime.datetime.now())

def job3():
    print("job3", datetime.datetime.now())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

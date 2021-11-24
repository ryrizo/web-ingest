import requests
import time
from threading import Thread
from threading import current_thread
'''
Demo meant to demonstrate GIL constraints on cpu bound work vs io bound work in Python.

CPU Bound: If the CPU has to do something, GIL will only use one active thread on one core. Adding threads results
in same amount of work being done and there is no gain - some compute lost to orchestration.

IO Bound: If waiting on IO, the CPU idle time is taken advantage of and a new thread can use CPU to issue another call.
Additional tasks will complete when multi-threading in this case.
'''


def multithreading_demo(task):
    global start
    # Experiment 1: Start two threads that count for 2 seconds
    start = time.time()
    multi_threaded_task(3, task)
    print(f"E2E Latency: {time.time() - start}")

    # Experiment 2: Let one thread count for 2 seconds.
    start = time.time()
    multi_threaded_task(1, task)
    print(f"E2E Latency: {time.time() - start}")


def multi_threaded_task(num_threads, task):
    threads = [Thread(target=task, name=f"{i}Thread") for i in range(num_threads)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def cpu_work(x=2):
    while time.time() - start < 2:
        x += 1
    print(f"Completed {x} increments for thread {current_thread().getName()}")
    return x


def io_work():
    url = 'http://www.cfbstats.com/2021/team/37/scoring/offense/gamelog.html'
    calls = 0
    while time.time() - start < 2:
        requests.get(url)
        calls += 1
    print(f"completed {calls} calls for thread {current_thread().getName()}")
    return calls


if __name__ == '__main__':
    multithreading_demo(cpu_work)
    multithreading_demo(io_work)
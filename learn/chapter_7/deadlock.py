from threading import Lock, Thread
import time

lock_a = Lock()
lock_b = Lock()

def a():
    # Acquire lock A
    with lock_a:
        print('Acquired lock a from method a!')
        # Sleep for 1 sec; this ensures we create the right conditions for deadlock
        time.sleep(1)
        # Acquire lock B
        with lock_b:
            print('Acquired both locks from method a!')

def b():
    # Acquire lock B
    with lock_b:
        print('Acquired lock_b from method b!')
        # Acquire lock A
        with lock_a:
            print('Acquired both locks from method b!')


thread_1 = Thread(target=a)
thread_2 = Thread(target=b)
thread_1.start()
thread_2.start()
thread_1.join()
thread_2.join()

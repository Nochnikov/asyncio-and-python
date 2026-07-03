import time
from multiprocessing import Process

def count(count_to: int) -> int:
    start = time.time()
    counter = 0

    while counter < count_to:
        counter += 1

    end = time.time()

    print(f'Total time: {end - start} seconds, counting_to: {count_to}')

    return counter

if __name__ == '__main__':
    start = time.time()
    # Create a process to run the countdown function.
    to_one_hundred_million = Process(target=count, args=(100000000,))
    to_two_hundred_million = Process(target=count, args=(200000000,))

    # Starting the process. This method returns instantly.
    to_one_hundred_million.start()
    to_two_hundred_million.start()

    # Wait for the process to finish. This method blocks until the process is done
    to_one_hundred_million.join()
    to_two_hundred_million.join()

    end = time.time()

    print(f'Completed in {end - start}')
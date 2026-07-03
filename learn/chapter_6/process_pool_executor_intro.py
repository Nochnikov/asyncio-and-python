import time
from concurrent.futures import ProcessPoolExecutor


def count(count_to: int) -> int:
    start = time.time()
    counter = 0
    while counter < count_to:
        counter += 1

    end = time.time()
    print(f'Counting to {count_to} finished in {end - start} seconds')
    return counter


if __name__ == '__main__':
    with ProcessPoolExecutor() as process_pool:
        numbers = [1, 3, 5, 22, 100000000]
        # even though every counting has its own process the map method will still wait for all answers
        # in order to guarantee the order of the results. In orderings like in example
        # it's not noticeable, but if we changed the index of 1 and 100000000 we would see
        # that it would take much time to print all results.
        for result in process_pool.map(count, numbers):
            print(result)



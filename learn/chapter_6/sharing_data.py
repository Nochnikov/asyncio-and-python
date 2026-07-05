from multiprocessing import Value, Array, Process


def increment_value(shared_int: Value):
    with shared_int.get_lock():
        shared_int.value += 1

def increment_array(shared_array: Array):
    for index, integer in enumerate(shared_array):
        shared_array[index] = integer + 1

if __name__ == '__main__':
    """When non of the process shares the same memory object."""
    # integer = Value('i', 0)
    # integer_array = Array('i', [0, 0])
    #
    # procs = [
    #     Process(target=increment_value, args=(integer,)),
    #     Process(target=increment_array, args=(integer_array,))
    # ]
    #
    # [p.start() for p in procs]
    # [p.join() for p in procs]
    #
    # print(integer.value)
    # print(integer_array[:])

    """When the process shares the same memory object."""

    for _ in range(100):
        integer = Value('i', 0)
        # Race condition may accure
        process = [
            Process(target=increment_value, args=(integer,)),
            Process(target=increment_value, args=(integer,))
        ]

        [p.start() for p in process]
        [p.join() for p in process]

        print(integer.value)
        assert (integer.value == 2)
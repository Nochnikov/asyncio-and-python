from threading import RLock, Thread

list_lock = RLock()

def sum_list(int_list: list[int]) -> int:
    print('Waiting to acquire lock...')
    with list_lock:
        print('Acquiring lock...')
        if len(int_list) == 0:
            print('Finished summing list')
            return 0
        else:
            head, *tail = int_list
            print('Summing list...')
            return head + sum_list(tail)

thread = Thread(target=sum_list, args=([1, 2, 3, 4],))
thread.start()
thread.join()
